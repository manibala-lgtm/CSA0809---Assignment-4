from attendance_fest import process_folder

if __name__ == "__main__":
    files = [
        "department_ai.txt",
        "department_cse.txt",
        "department_eee.txt",
        "department_mech.txt",
        "department_civil.txt",  # Deliberately missing file test
    ]
    records, errors = process_folder("input", "output", files)
    print("Valid unique registrations:", len(records))
    print("Rejected, duplicate or missing-file issues:", len(errors))
    print("Output files created in output/")
