import os
import sys
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

# Settings
default_delay = 1      # seconds between API calls
max_retries = 3        # retry attempts

# Predefined error classes
ERROR_CLASSES = [
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

# Configure logging
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# Retry decorator for API calls
def retry_api(func):
    def wrapper(*args, **kwargs):
        for attempt in range(1, max_retries + 1):
            try:
                time.sleep(default_delay)
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"Attempt {attempt} failed: {e}")
        logging.error(f"Failed after {max_retries} attempts")
        return None
    return wrapper

class LogicalErrorClassifier:
    def __init__(self, input_dir: Path, output_dir: Path, api_key: str, batch_size: int):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.batch_size = batch_size
        # Configure API key and model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def create_dirs(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def list_files(self):
        return sorted(self.input_dir.glob('*.py'))

    def read_code(self, path: Path) -> str:
        return path.read_text(encoding='utf-8')

    def build_batch_prompt(self, batch_paths):
        parts = [
            "You are a code debugging assistant. For each program below, classify any logical errors into the 14 error classes listed. Return a JSON mapping filenames to lists of error classes.",
            json.dumps(ERROR_CLASSES),
            "Programs:"
        ]
        for p in batch_paths:
            code = self.read_code(p)
            parts.append(f"{p.name}:```python\n{code}\n```")
        return "\n".join(parts)

    @retry_api
    def classify_batch(self, prompt: str):
        resp = self.model.generate_content(prompt)
        return resp.text.strip()

    def process(self):
        results = {}
        files = self.list_files()
        if not files:
            logging.info("No Python files to classify.")
            return
        logging.info(f"Classifying {len(files)} files in batches of {self.batch_size}...")
        for i in range(0, len(files), self.batch_size):
            batch = files[i:i+self.batch_size]
            prompt = self.build_batch_prompt(batch)
            raw = self.classify_batch(prompt)
            if raw is None:
                raw = '{}'
            try:
                batch_res = json.loads(raw)
            except json.JSONDecodeError:
                logging.error(f"Failed to parse response: {raw}")
                batch_res = {}
            for p in batch:
                results[p.name] = batch_res.get(p.name, [])
        self.save_and_report(results)

    def save_and_report(self, results):
        out_file = self.output_dir / 'classified_errors.json'
        with out_file.open('w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        logging.info(f"Saved results to {out_file}")
        table = [[fn, ', '.join(errs) if errs else 'None'] for fn, errs in results.items()]
        print(tabulate(table, headers=['Program','Errors'], tablefmt='grid'))

if __name__ == '__main__':
    configure_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', type=Path, default=Path('python_programs'), help='Directory of Python files')
    parser.add_argument('-o','--output', type=Path, default=Path('output'), help='Directory to save results')
    parser.add_argument('-k','--key', type=str, default=os.getenv('GOOGLE_API_KEY'), help='Gemini API key')
    parser.add_argument('-b','--batch', type=int, default=5, help='Batch size for API calls')
    args = parser.parse_args()

    if not args.key:
        logging.error("Provide API key via -k or GOOGLE_API_KEY env.")
        sys.exit(1)

    classifier = LogicalErrorClassifier(
        args.input, args.output, args.key,
        batch_size=args.batch
    )
    classifier.create_dirs()
    classifier.process()
