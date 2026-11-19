from pathlib import Path

def read_department_file(path, errors):
    records = []
    try:
        with Path(path).open("r", encoding="utf-8") as source:
            for line_number, line in enumerate(source, start=1):
                if not line.strip():
                    continue
                fields = [part.strip() for part in line.rstrip("\n").split(",")]
                if len(fields) != 5:
                    errors.append((str(path), line_number,
                                   f"expected 5 fields, found {len(fields)}"))
                    continue
                reg_no, name, department, email, event_text = fields
                records.append({
                    "register_number": reg_no,
                    "name": name,
                    "department": department,
                    "email": email,
                    "events": [event.strip() for event in event_text.split(";") if event.strip()],
                    "source": Path(path).name,
                    "line": line_number
                })
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as error:
        errors.append((str(path), 0, f"{type(error).__name__}: {error}"))
    return records
