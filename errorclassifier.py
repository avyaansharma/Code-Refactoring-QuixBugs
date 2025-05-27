import os
import sys
import glob
import argparse
import logging
import time
import json
from pathlib import Path
from tabulate import tabulate
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (optional)
load_dotenv()

# Models and settings
GOOGLE_MODEL = 'gemini-2.0-flash'
default_delay = 2 
default_temperature = 0
max_retries = 3

# Configure logging
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# Decorator for API error handling and retries
def handle_api_errors(func):
    def wrapper(*args, **kwargs):
        for attempt in range(1, max_retries + 1):
            try:
                time.sleep(default_delay)
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"API call failed (attempt {attempt}/{max_retries}): {e}")
        logging.error(f"All {max_retries} attempts failed for {func.__name__}")
        return None
    return wrapper

class LogicalErrorClassifier:
    """
    Agent to classify logical errors in Python programs using Gemini 2.0 Flash.
    """
    def __init__(self, input_dir: Path, output_dir: Path, api_key: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(GOOGLE_MODEL)

        # Define error classes
        self.error_classes = [
            "Off-by-one error",
            "Incorrect loop condition",
            "Wrong arithmetic operator",
            "Wrong comparison operator",
            "Incorrect variable update",
            "Missing edge case handling",
            "Incorrect function call",
            "Mismatched data structure usage",
            "Unintended infinite loop",
            "Premature return or exit",
            "Wrong initial condition",
            "Incorrect recursion base case",
            "Incorrect condition in if/elif",
            "Logic inversion (e.g., using `not` when not needed)"
        ]

    def create_directories(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_python_files(self):
        return list(self.input_dir.glob('*.py'))

    def read_file(self, path: Path) -> str:
        return path.read_text(encoding='utf-8')

    @handle_api_errors
    def classify_errors(self, code: str, filename: str) -> list:
        prompt = f"""
You are a code debugging assistant. Analyze the following Python program and classify any logical errors you find into one or more of the following 14 error classes:
{json.dumps(self.error_classes, indent=2)}

Program name: {filename}
Code:
```python
{code}
```

Return a JSON list of the error class names found in the program. If no errors are found, return an empty list.
"""
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logging.warning(f"Could not parse JSON for {filename}. Response was:\n{text}\n")
            return []

    def save_results(self, results: dict):
        out_file = self.output_dir / 'classified_errors.json'
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        logging.info(f"Results saved to {out_file}")

    def print_summary(self, results: dict):
        table = []
        for fname, errs in results.items():
            summary = ", ".join(errs) if errs else "No logical errors found"
            table.append([fname, summary])
        print(tabulate(table, headers=["Program", "Error Classes"], tablefmt="grid"))

    def process_all(self):
        results = {}
        files = self.get_python_files()
        if not files:
            logging.info(f"No Python files found in {self.input_dir}")
            return
        logging.info(f"Found {len(files)} files to classify in {self.input_dir}")

        for path in files:
            logging.info(f"Classifying errors in {path.name}")
            code = self.read_file(path)
            errs = self.classify_errors(code, path.name) or []
            results[path.name] = errs

        self.save_results(results)
        self.print_summary(results)


def main():
    configure_logging()
    parser = argparse.ArgumentParser(description="Classify logical errors in Python programs with Gemini Flash")
    parser.add_argument('-i', '--input', type=Path, default=Path('python_programs'), help="Folder of Python programs to classify")
    parser.add_argument('-o', '--output', type=Path, default=Path('output'), help="Folder to save results")
    parser.add_argument('-k', '--key', type=str, default=os.getenv('GOOGLE_API_KEY'), help="Gemini API key (or set GOOGLE_API_KEY env)")
    args = parser.parse_args()

    if not args.key:
        logging.error("Please provide a GOOGLE API key via -k or GOOGLE_API_KEY env variable.")
        sys.exit(1)

    agent = LogicalErrorClassifier(args.input, args.output, args.key)
    agent.create_directories()
    agent.process_all()

if __name__ == '__main__':
    main()
