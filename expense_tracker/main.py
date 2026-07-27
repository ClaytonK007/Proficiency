from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import date
from database import *
from chart import generate_category_chart

app = FastAPI()
templates = Jinja2Templates(directory="templates")
init_db()


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