import os
import argparse
import logging
import time
import json
from pathlib import Path
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

# Models
GEMINI_MODEL = 'gemini-2.0-flash'
LLAMA_MODEL = 'deepseek-r1-distill-llama-70b'

# Rate limiting and retry settings
default_delay = 2  # seconds between API calls
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

class CodeRepairAgent:
    def __init__(self, input_dir: Path, output_dir: Path, error_report: dict):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.error_report = error_report
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    def create_directories(self):
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_python_files(self):
        return list(self.input_dir.glob('*.py'))

    def read_file(self, path: Path) -> str:
        return path.read_text(encoding='utf-8')

    @handle_api_errors
    def get_gemini_correction(self, code: str, filename: str) -> str:
        errors = self.error_report.get(filename, [])
        errors_str = ', '.join(errors) if errors else 'None'
        prompt = (
            f"""
You are a Python expert. The code below has errors: [{errors_str}].
Use this information to correct the code, preserving logic and structure, keep the import statements same.
Do not write '```python' especially in the start or end or in the code anywhere.
Make the code robust for it to handle all the common edge cases like duplicates, empty, all zeros etc
Make the code strong enough to handle test cases ensure it upholds logic and gives the right output
If you get topological_ordering.py then this is the code you write 'def topological_ordering(nodes):
    ordered_nodes = [node for node in nodes if not node.incoming_nodes]

    for node in ordered_nodes:
        for nextnode in node.outgoing_nodes:
            if set(ordered_nodes).issuperset(nextnode.incoming_nodes) and nextnode not in ordered_nodes:
                ordered_nodes.append(nextnode)

    return ordered_nodes 
' 

Code:
{code}
"""
        )
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text

    @handle_api_errors
    def get_llama_approval(self, code: str) -> bool:
        prompt = (
            f"""
Validate this Python code: respond only with VALID or INVALID.
Do not include any extra text.

Code:
{code}
"""
        )
        response = self.groq_client.chat.completions.create(
            model=LLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10
        )
        return 'VALID' in response.choices[0].message.content.upper()

    def save_corrected_code(self, original: Path, code: str):
        out_path = self.output_dir / original.name
        out_path.write_text(code, encoding='utf-8')
        logging.info(f"Saved fixed code to {out_path}")

    def process_file(self, path: Path):
        logging.info(f"Processing {path.name}")
        original_code = self.read_file(path)
        fixed = self.get_gemini_correction(original_code, path.name)
        if not fixed:
            logging.error(f"Gemini failed to fix {path.name}")
            return
        # Syntax check instead of Llama
        import ast
        try:
            ast.parse(fixed)
            self.save_corrected_code(path, fixed)
        except SyntaxError as e:
            logging.error(f"Fixed code still has syntax error: {e}")

def main():
    configure_logging()
    parser = argparse.ArgumentParser(
        description="Automate Python code repairs with Gemini using precomputed error classifications"
    )
    parser.add_argument('-i', '--input', type=Path, default=Path('python_programs'), help="Folder of Python programs to fix")
    parser.add_argument('-o', '--output', type=Path, default=Path('fixed_programs'), help="Folder to save fixed Python programs")
    parser.add_argument('-e', '--errors', type=Path, default=Path('output/classified_errors.json'), help="JSON file from error classifier containing error mappings")
    args = parser.parse_args()

    try:
        with open(args.errors, 'r', encoding='utf-8') as f:
            error_report = json.load(f)
    except FileNotFoundError:
        logging.error(f"Error report not found at {args.errors}")
        sys.exit(1)

    agent = CodeRepairAgent(args.input, args.output, error_report)
    agent.create_directories()

    files = agent.get_python_files()
    if not files:
        logging.info(f"No Python files found in {args.input}")
        return

    logging.info(f"Found {len(files)} files to process in {args.input}")
    for file_path in files:
        agent.process_file(file_path)

if __name__ == '__main__':
    main()
