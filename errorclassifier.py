import os
import sys
import argparse
import logging
import time
import json
import re
from pathlib import Path
from tabulate import tabulate
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Settings
default_delay = 8
max_retries = 3       

# Predefined error classes
ERROR_CLASSES = [
    "Incorrect assignment operator",
    "Incorrect variable",
    "Incorect comparison operator",
    "Missing condition",
    "Missing/added +1",
    "Variable swap",
    "Incorrect array slice",
    "Variable prepend",
    "Incorrect data structure constant",
    "Incorrect method called",
    "Incorrect field dereference",
    "Missing arithmetic expression",
    "Missing function call", 
    "Missing line"
]

# Configure logging
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


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
    def __init__(self, input_dir: Path, output_dir: Path, api_key: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        # Configure API key and model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def create_dirs(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def list_files(self):
        return sorted(self.input_dir.glob('*.py'))

    def read_code(self, path: Path) -> str:
        return path.read_text(encoding='utf-8')

    def build_prompt(self, filename: str, code: str) -> str:
        return (
            "You are a code debugging assistant. Classify any logical errors in the program "
            "into the 14 error classes listed below.\n\n"
            "ERROR CLASSES:\n" + 
            "\n".join(f"- {ec}" for ec in ERROR_CLASSES) + 
            "\n\nReturn ONLY a JSON array containing the error classes that apply to this program. "
            "Do not include any other text or explanations.\n\n"
            f"Program: {filename}\n"
            f"Code:\n```python\n{code}\n```"
        )

    @retry_api
    def classify_file(self, prompt: str):
        resp = self.model.generate_content(prompt)
        return resp.text.strip()

    def extract_json(self, text: str):
        """Extract JSON array from response"""
        try:
            # First try to parse directly
            return json.loads(text)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from markdown code block
            match = re.search(r'```(?:json)?\n(.*?)\n```', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON-like substring
            start = text.find('[')
            end = text.rfind(']')
            if start > -1 and end > start:
                try:
                    return json.loads(text[start:end+1])
                except json.JSONDecodeError:
                    pass
            
        logging.error(f"Could not extract JSON from: {text[:200]}...")
        return []

    def process(self):
        results = {}
        files = self.list_files()
        if not files:
            logging.info("No Python files to classify.")
            return
            
        logging.info(f"Classifying {len(files)} files individually...")
        
        for file in files:
            filename = file.name
            logging.info(f"Processing {filename}...")
            
            code = self.read_code(file)
            prompt = self.build_prompt(filename, code)
            raw = self.classify_file(prompt)
            
            if raw is None:
                errors = []
            else:
                errors = self.extract_json(raw)
                
            # Validate the errors are from our predefined list
            valid_errors = []
            for err in errors:
                if err in ERROR_CLASSES:
                    valid_errors.append(err)
                else:
                    logging.warning(f"Invalid error class '{err}' found for {filename}")
            
            results[filename] = valid_errors
            logging.info(f"Classified {filename}: {valid_errors if valid_errors else 'No errors'}")
        
        self.save_and_report(results)

    def save_and_report(self, results):
        out_file = self.output_dir / 'classified_errors.json'
        with out_file.open('w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        logging.info(f"Saved results to {out_file}")
        
        # Prepare table for display
        table_data = []
        for filename, errors in results.items():
            table_data.append([filename, ', '.join(errors) if errors else 'None'])
        
        print(tabulate(table_data, headers=['Program', 'Errors'], tablefmt='grid'))

if __name__ == '__main__':
    configure_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', type=Path, default=Path('python_programs'), help='Directory of Python files')
    parser.add_argument('-o','--output', type=Path, default=Path('output'), help='Directory to save results')
    parser.add_argument('-k','--key', type=str, default=os.getenv('GOOGLE_API_KEY'), help='Gemini API key')
    args = parser.parse_args()

    if not args.key:
        logging.error("Provide API key via -k or GEMINI_API_KEY env.")
        sys.exit(1)

    classifier = LogicalErrorClassifier(args.input, args.output, args.key)
    classifier.create_dirs()
    classifier.process()