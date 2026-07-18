from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from model import User
from db_config import engine, get_db
import db_model
from validation import *

#   1. Create instance to initialize Fast API.
#   2. Configure backend to communicate with frontend.
#   3. Set template directory to render HTML templates for the frontend.
app = FastAPI()
db_model.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


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

    if not validate_name(name):
        return templates.TemplateResponse(
            request,
            "error.html",
            {"error": "Name must be at least 2 letters long and contain no numbers."},
        )

    if not validate_name(surname):
        return templates.TemplateResponse(
            request,
            "error.html",
            {"error": "Surname must be at least 2 letters long and contain no numbers."},
        )

    if not validate_south_african_id(idNo):
        return templates.TemplateResponse(
            request,
            "error.html",
            {"error": "ID number must be a valid South African ID number with 13 digits."},
        )

    if not validate_dob_matches_id(dob, idNo):
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