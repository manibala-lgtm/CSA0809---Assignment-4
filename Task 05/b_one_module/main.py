from pathlib import Path
from attendance_utils import read_attendance, percentage, consecutive_absentees, write_report

if __name__ == "__main__":
    source = Path("attendance.txt")
    lines = source.read_text(encoding="utf-8").splitlines()
    records = read_attendance(lines)
    results = percentage(records)
    write_report(results, "percentage_report.txt")
    print(results)
    print("Absent three consecutive days:", consecutive_absentees(records))
