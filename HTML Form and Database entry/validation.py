from datetime import datetime

#   Validate South African ID number to correctly match the date of birth provided in the form submission.
def validate_south_african_id(id_no: str) -> bool:
    if len(id_no) != 13 or not id_no.isdigit():
        return False

    try:
        birth_date = datetime.strptime(id_no[:6], "%y%m%d").date()
    except ValueError:
        return False

    return True


def validate_dob_matches_id(dob: str, id_no: str) -> bool:
    if not validate_south_african_id(id_no):
        return False

    try:
        parsed_dob = datetime.strptime(dob, "%d-%m-%Y").date()
    except ValueError:
        return False

    id_birth_date = datetime.strptime(id_no[:6], "%y%m%d").date()
    return parsed_dob.year == id_birth_date.year and parsed_dob.month == id_birth_date.month and parsed_dob.day == id_birth_date.day

#   Validate name and surname to ensure they are at least 2 letters long, contain no numbers and no special characters.
def validate_name(value: str) -> bool:
    if not value or not value.strip():
        return False

    cleaned = value.strip()

    if len(cleaned) < 2:
        return False

    if any(not char.isalpha() for char in cleaned):
        return False

    return True