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
                time.sleep(5)
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"API call failed (attempt {attempt}/3): {e}")
        logging.error(f"All 3 attempts failed for {func.__name__}")
        return None
    return wrapper

class CodeRepairAgent:
    def __init__(self, input_dir: Path, output_dir: Path, error_report: dict, testcases: dict):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.error_report = error_report
        self.testcases = testcases
        api_key = os.getenv('GEMINI_API_KEY')
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

    @handle_api_errors
    def get_gemini_correction(self, code: str, filename: str, failure_report: str, cases: list) -> str:
        errors = self.error_report.get(filename, [])
        errors_str = ', '.join(errors) if errors else 'None'
        parts = [
            "You are a Python expert and an expert in Data structures and algorithms in Python. The function below must pass all provided testcases.",
            f"You are told that the code below has errors: [{errors_str}], your job is to fix them as good as you can. "
            f"Previously it failed these checks:\n{failure_report}" if failure_report else None,
            "Testcases (input => expected):"
        ]
        for c in cases:
            parts.append(f"{c['input']} => {c['expected']}")
        parts.extend([
            f"Original code ({filename}):\n{code}",
            "Return only the full corrected code, no markdown formatting."
        ])
        prompt = "\n\n".join(p for p in parts if p)
        resp = self.model.generate_content(prompt)
        return resp.text

    def process_file(self, path: Path):
        logging.info(f"Processing {path.name}")
        original = self.read_file(path)
        cases = self.testcases.get(path.name, [])
        failure_report = ""

        # If no testcases, just syntax-fix once
        if not cases:
            fixed = self.get_gemini_correction(original, path.name, failure_report, [])
            if fixed and self.is_valid_python(fixed):
                self.save_corrected_code(path, fixed)
            return

        # Iterative test-driven repair
        last_fixed = None
        for attempt in range(3):
            fixed = self.get_gemini_correction(original, path.name, failure_report, cases)
            last_fixed = fixed or last_fixed
            if not fixed or not self.is_valid_python(fixed):
                continue

            # Execute and validate testcases
            namespace = {}
            try:
                exec(fixed, namespace)
                func = namespace.get(path.stem)
                failures = []
                for c in cases:
                    inp = c['input']
                    got = func(inp)
                    if got != c['expected']:
                        failures.append(f"Input={inp!r} => got {got!r}, want {c['expected']!r}")
            except Exception as e:
                failures = [f"Runtime error: {e}"]

            if not failures:
                self.save_corrected_code(path, fixed)
                return

            failure_report = "\n".join(failures)
            logging.info(f"Attempt {attempt+1} failed for {path.name}: {failure_report}")

        # All attempts failed: save last fix or original for inspection
        failed_path = self.output_dir / '_failed' / path.name
        content_to_save = last_fixed if last_fixed else original
        failed_path.write_text(content_to_save, encoding='utf-8')
        logging.error(f"All attempts failed for {path.name}. Last version saved to {failed_path}")

    def save_corrected_code(self, original: Path, code: str):
        out_path = self.output_dir / original.name
        out_path.write_text(code, encoding='utf-8')
        logging.info(f"Saved corrected code to {out_path}")


def main():
    configure_logging()
    parser = argparse.ArgumentParser(description="Test-driven code repair with Gemini")
    parser.add_argument('-i','--input', type=Path, default=Path('python_programs'), help='Input directory')
    parser.add_argument('-o','--output', type=Path, default=Path('fixed_programs'), help='Output directory')
    parser.add_argument('-e', '--errors', type=Path, default=Path('output/classified_errors.json'), help="JSON file from error classifier containing error mappings")
    parser.add_argument('-c','--cases', type=Path, default=Path('json_testcases.json'), help='Testcases JSON')
    args = parser.parse_args()

    # Load error report
    if not args.errors.exists():
        logging.error(f"Error report file not found: {args.errors}")
        sys.exit(1)
    try:
        error_report = json.loads(args.errors.read_text(encoding='utf-8'))
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in error report: {e}")
        sys.exit(1)

    # Load testcases
    testcases = {}
    if not args.cases.exists():
        logging.warning(f"Testcases file not found: {args.cases}. Continuing without test-driven repair.")
    else:
        try:
            testcases = json.loads(args.cases.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in testcases file: {e}")
            sys.exit(1)

    agent = CodeRepairAgent(args.input, args.output, error_report, testcases)
    agent.create_directories()

    files = agent.get_python_files()
    if not files:
        logging.info("No Python files to process.")
        sys.exit(0)

    logging.info(f"Found {len(files)} files to process in {args.input}")
    for path in files:
        agent.process_file(path)

if __name__ == '__main__':
    main()
