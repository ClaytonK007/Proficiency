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


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user_by_username(username)
    if not user or not verify_password(password, user["password_hash"]):
        return templates.TemplateResponse(
            request, "login.html", {"error": "Invalid username or password."}
        )


@app.post("logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/")
def index(request: Request, chart_type: str = "pie"):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    today = date.today()
    month_start = today.replace(day=1).isoformat()
    month_end = today.isoformat()

    expenses = get_expenses(user_id)
    category_totals = get_category_totals(user_id, start_date=month_start, end_date=month_end)
    total_spent = get_total_spent(user_id, start_date=month_start, end_date=month_end)
    monthly_totals = get_monthly_totals(user_id)

    chart_image = generate_category_chart(category_totals, chart_type=chart_type)
    trend_image = generate_monthly_trend_chart(monthly_totals)

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "expenses": expenses,
            "category_totals": category_totals,
            "total_spent": total_spent,
            "chart_image": chart_image,
            "trend_image": trend_image,
            "chart_type": chart_type,
            "categories": CATEGORIES,
            "today": today().isoformat(),
            "username": request.session.get("username")
        }
    )


@app.post("/add")
def add_expense_route(
    request: Request,
    description: str = Form(...),
    category: str = Form(...),
    amount: float = Form(...),
    expense_date: str = Form(...)
):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)
    add_expense(user_id, description.strip(), category, amount, expense_date)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{expense_id}")
def delete_expense_route(expense_id: int):
    user_id = get_current_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)
    delete_expense(user_id, expense_id)
    return RedirectResponse(url="/", status_code=303)