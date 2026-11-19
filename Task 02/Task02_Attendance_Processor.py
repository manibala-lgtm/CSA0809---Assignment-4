"""Task 2 - Monthly biometric attendance processor.
Run: python Task02_Attendance_Processor.py
Input: daily CSV-like text files in input/
Outputs: attendance_summary.csv and damaged_lines.txt
"""
from pathlib import Path
from collections import defaultdict
import csv

INPUT_DIR = Path("input")
SUMMARY_FILE = Path("attendance_summary.csv")
ERROR_FILE = Path("damaged_lines.txt")

def process_month(input_dir=INPUT_DIR, summary_path=SUMMARY_FILE, error_path=ERROR_FILE):
    counts = defaultdict(lambda: {"P": 0, "A": 0})
    errors = []
    files = sorted(Path(input_dir).glob("*.txt"))

    for path in files:
        try:
            with path.open("r", encoding="utf-8") as source:
                for line_no, line in enumerate(source, start=1):
                    if not line.strip():
                        continue
                    fields = [part.strip() for part in line.strip().split(",")]
                    if len(fields) != 3:
                        errors.append(f"{path.name},{line_no},expected 3 fields")
                        continue
                    reg_no, date, status = fields
                    if status not in {"P", "A"}:
                        errors.append(f"{path.name},{line_no},invalid status {status!r}")
                        continue
                    counts[reg_no][status] += 1
        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as error:
            errors.append(f"{path.name},0,{type(error).__name__}: {error}")

    with summary_path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["Register Number", "Present", "Absent", "Working Days", "Attendance %"])
        for reg_no in sorted(counts):
            present = counts[reg_no]["P"]
            absent = counts[reg_no]["A"]
            total = present + absent
            percentage = (present / total * 100) if total else 0.0
            writer.writerow([reg_no, present, absent, total, f"{percentage:.2f}"])

    with error_path.open("w", encoding="utf-8") as output:
        output.write("File,Line,Problem\n")
        for error in errors:
            output.write(error + "\n")

    below_75 = [
        (reg_no, counts[reg_no]["P"] / sum(counts[reg_no].values()) * 100)
        for reg_no in counts
        if sum(counts[reg_no].values()) and
        counts[reg_no]["P"] / sum(counts[reg_no].values()) * 100 < 75
    ]
    return counts, below_75, errors

if __name__ == "__main__":
    counts, below, errors = process_month()
    print("Students processed:", len(counts))
    print("Below 75%:", below)
    print("Damaged or inaccessible input records:", len(errors))
