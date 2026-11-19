"""Task 1.2 - Repaired hostel mess bill processor.
Run: python Task01_Repair_Mess_Bills.py [optional_input_file]
"""
from pathlib import Path
import sys

def process_mess_bills(filename):
    total = 0.0
    report_rows = []
    rejected_lines = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = [part.strip() for part in line.split(",")]
                try:
                    if len(parts) != 3:
                        raise ValueError(f"expected 3 fields, found {len(parts)}")
                    register_number, name, amount_text = parts
                    amount = float(amount_text)
                    report_rows.append(f"{register_number} | {name} | {amount:.2f}")
                    total += amount
                except ValueError as error:
                    rejected_lines.append((line_number, line, str(error)))
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as error:
        print(f"Could not process {filename}: {error}")
        return None

    print("\n".join(report_rows))
    print(f"Total: {total:.2f}")
    print("Rejected lines:")
    for item in rejected_lines:
        print(item)
    return total, report_rows, rejected_lines

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "mess_oct.txt"
    process_mess_bills(input_file)
