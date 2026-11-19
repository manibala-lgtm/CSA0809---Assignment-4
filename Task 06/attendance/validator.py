def valid_email(email):
    email = email.strip()
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain or " " in email:
        return False
    if "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    return True

def validate_record(record):
    required = ("register_number", "name", "department", "email")
    if any(not record[key] for key in required):
        return False, "required field is empty"
    if not valid_email(record["email"]):
        return False, "invalid email address"
    if not record["events"]:
        return False, "no event selected"
    return True, ""
