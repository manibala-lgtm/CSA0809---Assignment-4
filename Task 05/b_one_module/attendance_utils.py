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
    return {reg: 100 * v["P"] / (v["P"] + v["A"]) for reg, v in stats.items()}

def consecutive_absentees(records):
    by_student = {}
    for reg, date, status in records:
        by_student.setdefault(reg, {})[date] = status
    return [reg for reg, days in by_student.items()
            if any(sorted(days.items())[i][1] == sorted(days.items())[i+1][1] ==
                   sorted(days.items())[i+2][1] == "A"
                   for i in range(max(0, len(days)-2)))]

def write_report(values, path):
    with open(path, "w", encoding="utf-8") as file:
        for key, value in values.items():
            file.write(f"{key},{value:.2f}\n")
