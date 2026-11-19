def read_attendance(lines):
    records = []
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 3 and parts[2] in {"P", "A"}:
            records.append(tuple(parts))
    return records
