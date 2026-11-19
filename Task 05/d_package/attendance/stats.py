def percentage(records):
    counts = {}
    for reg, date, status in records:
        counts.setdefault(reg, {"P": 0, "A": 0})
        counts[reg][status] += 1
    return {reg: 100 * value["P"] / (value["P"] + value["A"])
            for reg, value in counts.items()}

def consecutive_absentees(records):
    by_student = {}
    for reg, date, status in records:
        by_student.setdefault(reg, {})[date] = status
    result = []
    for reg, days in by_student.items():
        ordered = [status for _, status in sorted(days.items())]
        if any(ordered[i:i+3] == ["A", "A", "A"] for i in range(len(ordered)-2)):
            result.append(reg)
    return result
