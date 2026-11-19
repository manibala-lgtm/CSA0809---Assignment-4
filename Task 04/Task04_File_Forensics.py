"""Task 4 - Demonstrate file defects and show repaired file handling.
Run: python Task04_File_Forensics.py
"""
from pathlib import Path
import tempfile

def demonstrate_bad_save(books, log_path):
    # Deliberately defective: write mode truncates earlier content and no newlines are added.
    log = open(log_path, "w", encoding="utf-8")
    for book in books:
        log.write(book)
    log.close()

def demonstrate_bad_process(day_file, log_path):
    try:
        books = open(day_file, "r", encoding="utf-8").read().split("\n")
        demonstrate_bad_save(books, log_path)
    except FileNotFoundError:
        print("missing")

def save_returns(books, log_path="returns.log"):
    with open(log_path, "a", encoding="utf-8") as log:
        for book in books:
            if book.strip():
                log.write(book.rstrip() + "\n")

def process(day_file, log_path="returns.log", error_log="returns_errors.log"):
    try:
        with open(day_file, "r", encoding="utf-8") as source:
            books = source.read().splitlines()
        save_returns(books, log_path)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as error:
        with open(error_log, "a", encoding="utf-8") as errors:
            errors.write(f"{day_file}: {type(error).__name__}: {error}\n")

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        log = folder / "returns.log"
        day_files = []
        for day, books in enumerate((["Book A", "Book B"], ["Book C"], ["Book D", "Book E"]), start=1):
            path = folder / f"day{day}.txt"
            path.write_text("\n".join(books), encoding="utf-8")
            day_files.append(path)

        print("Defective version:")
        for path in day_files:
            demonstrate_bad_process(path, log)
            print(log.read_text(encoding="utf-8"))

        log.write_text("", encoding="utf-8")
        print("Repaired version:")
        for path in day_files:
            process(path, log, folder / "errors.log")
        process(folder / "missing.txt", log, folder / "errors.log")
        print(log.read_text(encoding="utf-8"))
        print("Error log:")
        print((folder / "errors.log").read_text(encoding="utf-8"))
