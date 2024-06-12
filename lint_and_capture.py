import os
import subprocess
from datetime import datetime
from gitignore_parser import parse_gitignore

# Directory to save linting reports
REPORT_DIR = "lint_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# List of files and directories to ignore
EXCLUDE_FILES = [
    "settings.py",
    "initial.py",
    "migrations"
]


def should_ignore(file_path):
    for exclude in EXCLUDE_FILES:
        if exclude in file_path:
            return True
    return False


def find_python_files(directory):
    # Parse .gitignore
    gitignore_path = os.path.join(directory, ".gitignore")
    matches = (
        parse_gitignore(gitignore_path)
        if os.path.exists(gitignore_path)
        else lambda x: False
    )

    # Find all .py files in the directory and subdirectories
    py_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                if not matches(file_path) and not should_ignore(file_path):
                    py_files.append(file_path)
    return py_files


def run_flake8(files):
    # Run flake8 on the list of files and capture the output
    result = subprocess.run(
        ["flake8"] + files, capture_output=True, text=True
    )
    return result.stdout


def save_report(report):
    # Save the report to a text file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORT_DIR, f"flake8_report_{timestamp}.txt")
    with open(report_path, "w") as report_file:
        report_file.write(report)
    return report_path


if __name__ == "__main__":
    # Root directory of the project
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

    py_files = find_python_files(PROJECT_DIR)
    report = run_flake8(py_files)
    report_path = save_report(report)
    print(f"Report saved to {report_path}")
