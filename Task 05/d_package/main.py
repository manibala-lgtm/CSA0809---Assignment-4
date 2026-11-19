from pathlib import Path
from attendance.reader import read_attendance
from attendance.stats import percentage, consecutive_absentees
from attendance.report import write_percentage_report, write_absent_report

if __name__ == "__main__":
    records = read_attendance(Path("attendance.txt").read_text(encoding="utf-8").splitlines())
    values = percentage(records)
    absent = consecutive_absentees(records)
    write_percentage_report(values, "percentage_report.txt")
    write_absent_report(absent, "three_day_absentees.txt")
    print(values)
    print(absent)
