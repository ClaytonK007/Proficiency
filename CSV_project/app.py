import csv
import io
import os
from datetime import datetime
from flask import Flask, render_template, request
from db import get_connection, create_table
from generate_csv import generate_csv

#   1. Create instance to initialize Flask.
#   2. Set upload folder destination
#   3. Create directory recursively for upload destination incase it does not exist
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#   Button to go back to "/"
def back_button(message):
    return f"""
    <p>{message}</p>
    <button type="button" onclick="history.back()">Go Back</button>
    """

#   Route to render template
@app.route("/")
def index():
    return render_template("index.html")

#   Route to generate csv file when form is submitted
@app.route("/generate", methods=["POST"])
def generate():
    count = int(request.form["count"])
    written = generate_csv(count)
    return back_button(f"Generated {written} records to 'output/output.csv'")

#   Route to import csv from form submitted
@app.route("/import", methods=["POST"])
def import_csv():
    file = request.files["csvfile"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    conn = get_connection()
    cur = conn.cursor()

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows_to_insert = []
        for row in reader:
            d, m, y = row["DateOfBirth"].split("/")
            dob_iso = f"{y}-{m}-{d}"
            rows_to_insert.append((
                row["Id"], row["Name"], row["Surname"], row["Initials"], row["Age"], dob_iso
            ))

        cur.executemany(
            "INSERT OR IGNORE INTO csv_import (Id, Name, Surname, Initials, Age, DateOfBirth) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            rows_to_insert
        )
        conn.commit()

    count_result = cur.execute("SELECT COUNT(*) FROM csv_import").fetchone()[0]
    conn.close()
    os.remove(filepath)

    return back_button(f"Import complete. Total records in table: {count_result}")

if __name__ == "__main__":
    create_table()
    app.run(debug=True, port=3000)