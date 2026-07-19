import csv
import os
import random
from datetime import date, timedelta
from data.names import NAMES, SURNAMES

#   Generate random age
def random_age():
    return random.randint(18, 65)

#   Generate random Date of Birth
def random_dob():
    start = date(1959, 1, 1).toordinal()
    end = date(2007, 12, 31).toordinal()
    d = date.fromordinal(random.randint(start, end))
    return d.strftime("%d/%m/%Y")

#   Generate CSV file
def generate_csv(count, output_path = os.path.join("output", "output.csv")):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    seen = set()
    written = 0

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(["Id", "Name", "Surname", "Initials", "Age", "DateOfBirth"])

        record_id = 1
        while written < count:
            name = random.choice(NAMES)
            surname = random.choice(SURNAMES)
            age = random_age()
            dob = random_dob()
            key = (name, surname, age, dob)

            if key in seen:
                continue #  ensures no duplicate rows

            seen.add(key)
            initials = (name[0] + surname[0]).upper()
            writer.writerow([record_id, name, surname, initials, age, dob])

            record_id += 1
            written += 1

    return written

if __name__ == "__main__":
    n = generate_csv(1_000_000)
    print(f"Generated {n} records.")