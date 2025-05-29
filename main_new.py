import os
import sys
import argparse
import logging
import time
import json
import ast
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables for API key
load_dotenv()

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# Retry decorator for API calls
def handle_api_errors(func):
    def wrapper(*args, **kwargs):
        for attempt in range(1, 4):
            try:
                time.sleep(10)
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"API call failed (attempt {attempt}/3): {e}")
        logging.error(f"All 3 attempts failed for {func.__name__}")
        return None
    return wrapper

class CodeRepairAgent:
    def __init__(
        self,
        input_dir: Path,
        output_dir: Path,
        error_report: dict,
        raw_cases: dict
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.error_report = error_report  # { filename.py: [error classes] }
        self.raw_cases = raw_cases        # { filename.py: [[input, expected], ...] }

        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            logging.error("Provide GEMINI_API_KEY in environment.")
            sys.exit(1)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def create_directories(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / '_failed').mkdir(parents=True, exist_ok=True)

    def get_python_files(self):
        return sorted(self.input_dir.glob('*.py'))

    def read_file(self, path: Path) -> str:
        return path.read_text(encoding='utf-8')

    def is_valid_python(self, code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError as e:
            logging.warning(f"Syntax error in generated code: {e}")
            return False

    def build_testcases(self, filename: str) -> list:
        """Load testcases directly from raw_cases: each entry is [input, expected]."""
        cases = []
        for pair in self.raw_cases.get(filename, []):
            inp, exp = pair
            cases.append({'input': inp, 'expected': str(exp)})
        return cases

    @handle_api_errors
    def get_gemini_correction(
        self,
        code: str,
        filename: str,
        failure_report: str,
        cases: list
    ) -> str:
        errors = self.error_report.get(filename, [])
        errors_str = ', '.join(errors) if errors else 'None'

        prompt_parts = [
            "You are a Python expert. The function below must pass all provided testcases.",
            f"Previously it failed these checks: {errors_str}",
            "You are the world's best in Data structures and algorithms in python, fix them according to your knowledge",
            f"Failure details:\n{failure_report}" if failure_report else "",
            "MUST NOT write '```python' at start or '```' at the end of the code, DONT EVER DO THIS"
            "The errors are in a single line of the code you must not change the code structure of the original code, try to only fix the errors by making minimal changes"
            "Keep the import statements same don't change them and try to keep the length of your code and the original code that you fix the same "
            "While going through the testcases if you don't get what you want rewrite the code accordingly but try to pass the testcases"
            "Testcases (input => expected):"
        ]
        for idx, c in enumerate(cases, 1):
            prompt_parts.append(f"Case {idx}: {c['input']} => {c['expected']}")
        prompt_parts.extend([
            f"Original code ({filename}):\n{code}",
            "Return only the full corrected Python code (no markdown)."
        ])
        prompt = "\n\n".join(p for p in prompt_parts if p)
        resp = self.model.generate_content(prompt)
        return resp.text

    def test_code(self, code: str, func_name: str, cases: list) -> tuple:
        """Execute `code` in isolated namespace, run `func_name` on each case."""
        namespace = {}
        try:
            exec(code, namespace)
        except Exception as e:
            return False, f"Execution error: {e}"

        func = namespace.get(func_name)
        if not func:
            return False, f"Function '{func_name}' not found"

        failures = []
        for c in cases:
            try:
                result = func(*c['input'])
            except Exception as e:
                failures.append(f"Input {c['input']} raised {type(e).__name__}: {e}")
                continue
            if str(result) != c['expected']:
                failures.append(f"Input {c['input']} => got {result!r}, want {c['expected']!r}")

        return (len(failures) == 0), "\n".join(failures)

    def process_file(self, path: Path):
        logging.info(f"Processing {path.name}")
        original = self.read_file(path)
        filename = path.name
        func_name = path.stem

        cases = self.build_testcases(filename)
        if not cases:
            logging.warning(f"No testcases for {filename}, skipping")
            return

        failure_report = ""
        current_code = original
        last_fixed = None
        for attempt in range(3):
            fixed = self.get_gemini_correction(current_code, filename, failure_report, cases)
            if not fixed:
                logging.warning(f"No fix returned for {filename} attempt {attempt+1}")
                continue
            last_fixed = fixed
            if not self.is_valid_python(fixed):
                failure_report = "Syntax errors in generated code"
                current_code = fixed
                continue

            success, report = self.test_code(fixed, func_name, cases)
            if success:
                self.save_corrected_code(path, fixed)
                logging.info(f"Repaired {filename} in {attempt+1} attempts")
                return

            failure_report = report
            current_code = fixed
            logging.info(f"Attempt {attempt+1} failed for {filename}: {report}")

        # All attempts failed
        out = last_fixed or original
        failed_path = self.output_dir / '_failed' / filename
        failed_path.write_text(out, encoding='utf-8')
        logging.error(f"All attempts failed for {filename}. Saved to {failed_path}")

    def save_corrected_code(self, original: Path, code: str):
        out_path = self.output_dir / original.name
        out_path.write_text(code, encoding='utf-8')
        logging.info(f"Saved corrected code to {out_path}")


def main():
    configure_logging()
    parser = argparse.ArgumentParser(description="Automated test-driven code repair with Gemini")
    parser.add_argument(
        '-i', '--input', type=Path,
        default=Path('python_programs'),
        help='Directory of buggy Python programs'
    )
    parser.add_argument(
        '-o', '--output', type=Path,
        default=Path('fixed_programs'),
        help='Directory to save fixed programs'
    )
    parser.add_argument(
        '-e', '--errors', type=Path,
        default=Path('output/classified_errors.json'),
        help='JSON file from errorclassifier.py'
    )
    parser.add_argument(
        '-t', '--testcases', type=Path,
        default=Path('json_testcases'),
        help='Directory containing per-file testcases JSON'
    )
    args = parser.parse_args()

    # Validate paths
    for p in [args.input, args.testcases]:
        if not p.exists():
            logging.error(f"Path not found: {p}")
            sys.exit(1)

    try:
        error_report = json.loads(args.errors.read_text(encoding='utf-8'))
    except Exception as e:
        logging.error(f"Failed to load error report: {e}")
        sys.exit(1)

    # Load raw cases
    raw_cases = {}
    for jf in args.testcases.glob('*.json'):
        try:
            lines = jf.read_text(encoding='utf-8').splitlines()
            parsed = [json.loads(line) for line in lines if line.strip()]
            raw_cases[jf.stem + '.py'] = parsed
        except Exception as e:
            logging.warning(f"Skipping invalid testcase file {jf}: {e}")

    agent = CodeRepairAgent(
        input_dir=args.input,
        output_dir=args.output,
        error_report=error_report,
        raw_cases=raw_cases
    )
    agent.create_directories()

    # If fixed_programs already has .py files, re-test/repair those;
    # otherwise process the original python_programs.
    if any(args.output.glob('*.py')):
        source_dir = args.output
        logging.info(f"Re-testing files in fixed directory: {source_dir}")
    else:
        source_dir = args.input
        logging.info(f"Testing files in input directory: {source_dir}")

    agent.input_dir = source_dir
    files = agent.get_python_files()
    if not files:
        logging.info("No Python files to process.")
        sys.exit(0)

    logging.info(f"Found {len(files)} files to process in {source_dir}")
    for path in files:
        agent.process_file(path)


if __name__ == '__main__':
    main()
