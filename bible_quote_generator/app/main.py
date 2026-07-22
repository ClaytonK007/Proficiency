from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models
from .database import engine, get_db
from .quotes_data import get_random_quote

app = FastAPI()
templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def index(request: Request):
    quote = get_random_quote()
    return templates.TemplateResponse(request, "index.html", {"quote": quote})

@app.post("/favourites/add")
def add_favourite(text: str = Form(...), reference: str = Form(...), db: Session = Depends(get_db)):
    favourite = models.Favourites(text=text, reference=reference)
    try:
        db.add(favourite)
        db.commit()
    except IntegrityError:
        db.rollback()
    return RedirectResponse(url="/favourites", status_code=303)

@app.get("/favourites")
def favourites(request: Request, db: Session = Depends(get_db)):
    favourites_list = db.query(models.Favourites).all()
    return templates.TemplateResponse(request, "favourites.html", {"favourites": favourites_list})

@app.post("/favourites/delete/{favourite_id}")
def remove_favourite(favourite_id: int, db: Session = Depends(get_db)):
    favourite = db.query(models.Favourites).filter(models.Favourites.id == favourite_id).first()
    if favourite:
        db.delete(favourite)
        db.commit()
    return RedirectResponse(url="/favourites", status_code=303)