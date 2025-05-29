<<<<<<< HEAD
import os
import glob
import argparse
import logging
import time
from pathlib import Path
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

# Models
GEMINI_MODEL = 'gemini-2.0-flash'
LLAMA_MODEL = 'meta-llama/llama-4-scout-17b-16e-instruct'

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
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
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
    def get_gemini_correction(self, code: str) -> str:
        prompt = (
            "Consider yourself a python expert who has a strong grasp of data structures and algorithms."
            "The code contains errors and you need to fix it properly, you have to ensure code is successfully compiled.  "
            "Return only the corrected code without explanations."
            "Keep in mind that you have to keep the logic and structure in the code intact."
            "Keep the import statements intact for the code you process. "
            "Also consider edge cases like elements being repeated or for an empty being an expert in DSA make sure it is robust to edge cases as well. "
            "Dont write '```python' or '```' anywhere in the code."
            f"\n\nCode:\n{code}"
        )
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text

    @handle_api_errors
    def get_llama_approval(self, code: str) -> bool:
        prompt = (
            "Consider that you are an expert in Python programming language and you have a lot of knowledge of data structures and algorithms."
            "Validate this Python code: respond only with 'VALID' or 'INVALID', dont give any explaination only 'VALID' or 'INVALID'."
            "Only output 'VALID' if the code will be successfully compiled. "
            "Only output 'VALID' if code preserves the original logic and doesn't make landmark changes like changing the import statements(an example)."
            f"\n\nCode:\n{code}"
        )
        response = self.groq_client.chat.completions.create(
            model=LLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10
        )
        return 'VALID' in response.choices[0].message.content.upper()

    def save_corrected_code(self, original: Path, code: str):
        fixed_name = f"{original.stem}.py"
        out_path = self.output_dir / fixed_name
        out_path.write_text(code, encoding='utf-8')
        logging.info(f"Saved fixed code to {out_path}")

    def process_file(self, path: Path):
        logging.info(f"Processing {path.name}")
        original_code = self.read_file(path)
        fixed = self.get_gemini_correction(original_code)
        if not fixed:
            logging.error(f"Gemini failed to fix {path.name}")
            return
        valid = self.get_llama_approval(fixed)
        if valid:
            self.save_corrected_code(path, fixed)
        else:
            logging.warning(f"Llama rejected fix for {path.name}")

def main():
    configure_logging()
    parser = argparse.ArgumentParser(
        description="Automate Python code repairs with Gemini & Llama"
    )
    parser.add_argument(
        '-i', '--input',
        type=Path,
        default=Path('python_programs'),
        help="Relative path to the folder of Python programs to fix"
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('fixed_programs'),
        help="Relative path to save fixed Python programs"
    )
    args = parser.parse_args()

    agent = CodeRepairAgent(args.input, args.output)
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
=======
import os
import glob
import argparse
import logging
import time
from pathlib import Path
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

# Models
GEMINI_MODEL = 'gemini-2.0-flash'
LLAMA_MODEL = 'meta-llama/llama-4-scout-17b-16e-instruct'

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
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
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
    def get_gemini_correction(self, code: str) -> str:
        prompt = (
            "Consider yourself a python expert who has a strong grasp of data structures and algorithms."
            "The code contains errors and you need to fix it properly, you have to ensure code is successfully compiled.  "
            "Return only the corrected code without explanations."
            "Keep in mind that you have to keep the logic and structure in the code intact."
            "Keep the import statements intact for the code you process. "
            "Also consider edge cases like elements being repeated or for an empty being an expert in DSA make sure it is robust to edge cases as well. "
            "Dont write '```python' or '```' anywhere in the code."
            f"\n\nCode:\n{code}"
        )
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text

    @handle_api_errors
    def get_llama_approval(self, code: str) -> bool:
        prompt = (
            "Consider that you are an expert in Python programming language and you have a lot of knowledge of data structures and algorithms."
            "Validate this Python code: respond only with 'VALID' or 'INVALID', dont give any explaination only 'VALID' or 'INVALID'."
            "Only output 'VALID' if the code will be successfully compiled. "
            "Only output 'VALID' if code preserves the original logic and doesn't make landmark changes like changing the import statements(an example)."
            f"\n\nCode:\n{code}"
        )
        response = self.groq_client.chat.completions.create(
            model=LLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10
        )
        return 'VALID' in response.choices[0].message.content.upper()

    def save_corrected_code(self, original: Path, code: str):
        fixed_name = f"{original.stem}.py"
        out_path = self.output_dir / fixed_name
        out_path.write_text(code, encoding='utf-8')
        logging.info(f"Saved fixed code to {out_path}")

    def process_file(self, path: Path):
        logging.info(f"Processing {path.name}")
        original_code = self.read_file(path)
        fixed = self.get_gemini_correction(original_code)
        if not fixed:
            logging.error(f"Gemini failed to fix {path.name}")
            return
        valid = self.get_llama_approval(fixed)
        if valid:
            self.save_corrected_code(path, fixed)
        else:
            logging.warning(f"Llama rejected fix for {path.name}")

def main():
    configure_logging()
    parser = argparse.ArgumentParser(
        description="Automate Python code repairs with Gemini & Llama"
    )
    parser.add_argument(
        '-i', '--input',
        type=Path,
        default=Path('python_programs'),
        help="Relative path to the folder of Python programs to fix"
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('fixed_programs'),
        help="Relative path to save fixed Python programs"
    )
    args = parser.parse_args()

    agent = CodeRepairAgent(args.input, args.output)
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
>>>>>>> 474d85f (Final changes)
