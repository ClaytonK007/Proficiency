from datetime import datetime
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from model import User
from db_config import engine, get_db
import db_model

#   1. Create instance to initialize Fast API.
#   2. Configure backend to communicate with frontend.
#   3. Set template directory to render HTML templates for the frontend.
app = FastAPI()
db_model.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


#   Validate South African ID number to correctly match the date of birth provided in the form submission.
def _validate_south_african_id(id_no: str) -> bool:
    if len(id_no) != 13 or not id_no.isdigit():
        return False

    try:
        birth_date = datetime.strptime(id_no[:6], "%y%m%d").date()
    except ValueError:
        return False

    return True


def _validate_dob_matches_id(dob: str, id_no: str) -> bool:
    if not _validate_south_african_id(id_no):
        return False

    try:
        parsed_dob = datetime.strptime(dob, "%d-%m-%Y").date()
    except ValueError:
        return False

    id_birth_date = datetime.strptime(id_no[:6], "%y%m%d").date()
    return parsed_dob.year == id_birth_date.year and parsed_dob.month == id_birth_date.month and parsed_dob.day == id_birth_date.day

#   Validate name and surname to ensure they are at least 2 letters long, contain no numbers and no special characters.
def _validate_name(value: str) -> bool:
    if not value or not value.strip():
        return False

    cleaned = value.strip()

    if len(cleaned) < 2:
        return False

    if any(not char.isalpha() for char in cleaned):
        return False

    return True


#   Display the form to add a new user
@app.get("/", response_class=HTMLResponse)
def load_home(request: Request):
    return templates.TemplateResponse(request, "index.html")


#   Get all users from the database
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(db_model.User).all()


#  Handle form submission and save user data to the database
@app.post("/submit", response_class=HTMLResponse)
def register_user(
    request: Request,
    name: str = Form(...),
    surname: str = Form(...),
    idNo: str = Form(...),
    dob: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        parsed_dob = datetime.strptime(dob, "%d-%m-%Y").date()
    except ValueError:
        return templates.TemplateResponse(
            request,
            "error.html",
            {"error": "Date of birth must be in DD-MM-YYYY format."},
        )

    if not _validate_name(name):
        return templates.TemplateResponse(
            request,
            "error.html",
            {"error": "Name must be at least 2 letters long and contain no numbers."},
        )

    if not _validate_name(surname):
        return templates.TemplateResponse(
            request,
            "error.html",
            {"error": "Surname must be at least 2 letters long and contain no numbers."},
        )

    if not _validate_south_african_id(idNo):
        return templates.TemplateResponse(
            request,
            "error.html",
            {"error": "ID number must be a valid South African ID number with 13 digits."},
        )

    if not _validate_dob_matches_id(dob, idNo):
        return templates.TemplateResponse(
            request,
            "error.html",
            {"error": "Date of birth does not match the first six digits of the ID number."},
        )

    existing_user = db.query(db_model.User).filter(db_model.User.idNo == idNo).first()
    if existing_user:
        return templates.TemplateResponse(
            request,
            "error.html",
            {"error": "User with this ID number already exists."},
        )

    new_user = db_model.User(name=name, surname=surname, idNo=idNo, dob=parsed_dob)
    db.add(new_user)
    db.commit()

    return templates.TemplateResponse(
        request,
        "confirmation.html",
        {"name": name, "surname": surname},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)