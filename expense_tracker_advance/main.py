from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from datetime import date
from database import *
from chart import generate_category_chart, generate_monthly_trend_chart

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="replace-with-a-real-random-secret")
templates = Jinja2Templates(directory="templates")
init_db()


def get_current_user(request: Request):
    return request.session.get("user_id")


@app.get("/register")
def register_form(request: Request):
    return templates.TemplateResponse(request, "register.html", {})

@app.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...)):
    if not create_user(username, password):
        return templates.TemplateResponse(
            request, "register.html", {"error": "That username is already taken"}
        )
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html", {})

@app.get("/")
def index(request: Request):
    expenses = get_expenses()
    category_totals = get_category_totals()
    total_spent = get_total_spent()
    chart_image = generate_category_chart(category_totals)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "expenses": expenses,
            "category_totals": category_totals,
            "total_spent": total_spent,
            "chart_image": chart_image,
            "categories": CATEGORIES,
            "today": date.today().isoformat()
        }
    )


@app.post("/add")
def add_expense_route(
    description: str = Form(...),
    category: str = Form(...),
    amount: float = Form(...),
    expense_date: str = Form(...)
):
    add_expense(description.strip(), category, amount, expense_date)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{expense_id}")
def delete_expense_route(expense_id: int):
    delete_expense(expense_id)
    return RedirectResponse(url="/", status_code=303)