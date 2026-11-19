def write_percentage_report(values, path):
    with open(path, "w", encoding="utf-8") as file:
        file.write("Register Number,Attendance Percentage\n")
        for reg, value in sorted(values.items()):
            file.write(f"{reg},{value:.2f}\n")

def write_absent_report(register_numbers, path):
    with open(path, "w", encoding="utf-8") as file:
        file.write("Register Number\n")
        for reg in sorted(register_numbers):
            file.write(reg + "\n")
