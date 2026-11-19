from pathlib import Path
import csv
from .reader import read_department_file
from .validator import validate_record

def process_folder(input_folder, output_folder, department_files):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    errors = []
    unique = {}
    for filename in department_files:
        path = input_folder / filename
        for record in read_department_file(path, errors):
            valid, reason = validate_record(record)
            if not valid:
                errors.append((record["source"], record["line"], reason))
                continue

            reg_no = record["register_number"]
            if reg_no in unique:
                errors.append((record["source"], record["line"],
                               f"duplicate registration {reg_no}; first record retained"))
                continue
            unique[reg_no] = record

    master_path = output_folder / "master_list.csv"
    with master_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Register Number", "Name", "Department", "Email", "Events"])
        for reg_no in sorted(unique):
            record = unique[reg_no]
            writer.writerow([reg_no, record["name"], record["department"],
                             record["email"], ";".join(record["events"])])

    event_participants = {}
    for record in unique.values():
        for event in record["events"]:
            event_participants.setdefault(event, []).append(record)

    for event, participants in event_participants.items():
        safe_name = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in event)
        with (output_folder / f"event_{safe_name}.txt").open("w", encoding="utf-8") as file:
            for record in sorted(participants, key=lambda item: item["register_number"]):
                file.write(f'{record["register_number"]},{record["name"]},{record["department"]}\n')

    with (output_folder / "summary_report.txt").open("w", encoding="utf-8") as file:
        file.write(f"Valid unique registrations: {len(unique)}\n")
        file.write(f"Events: {len(event_participants)}\n")
        for event, participants in sorted(event_participants.items()):
            file.write(f"{event}: {len(participants)} participants\n")
        file.write(f"Rejected or duplicate records: {len(errors)}\n")

    with (output_folder / "error_log.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["File", "Line", "Problem"])
        writer.writerows(errors)

    return unique, errors
