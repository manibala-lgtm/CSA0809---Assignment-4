"""Task 5(a) - All functions in one script."""
def read_attendance(lines):
    records = []
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 3 and parts[2] in {"P", "A"}:
            records.append(tuple(parts))
    return records

def percentage(records):
    stats = {}
    for reg, date, status in records:
        stats.setdefault(reg, {"P": 0, "A": 0})
        stats[reg][status] += 1
    return {reg: 100 * value["P"] / (value["P"] + value["A"])
            for reg, value in stats.items()}

def consecutive_absentees(records):
    by_student = {}
    for reg, date, status in records:
        by_student.setdefault(reg, {})[date] = status
    result = []
    for reg, days in by_student.items():
        ordered = sorted(days.items())
        if any(ordered[i][1] == ordered[i+1][1] == ordered[i+2][1] == "A"
               for i in range(len(ordered)-2)):
            result.append(reg)
    return result

def write_report(values, path):
    with open(path, "w", encoding="utf-8") as file:
        for key, value in values.items():
            file.write(f"{key},{value:.2f}\n")

if __name__ == "__main__":
    sample = ["192311001,2026-10-01,P", "192311001,2026-10-02,A",
              "192311001,2026-10-03,A", "192311001,2026-10-04,A"]
    records = read_attendance(sample)
    print(percentage(records))
    print("Absent three consecutive days:", consecutive_absentees(records))
