# Advanced Expense Tracker

## Requirements

- Allow a user to create an account
- Allow user to add expenses (description, category, amount, date) and delete expenses which only they will be able to edit and view
- Save data to database
- Display expenses on a table
- Display a live spending breakdown by category — updates automatically every time an expense is added or deleted. (Bar and Pie chart)

## How to deploy and test:
- download or pull project repository
- create a virtual environment in the repository - run "python -m venv .venv" in your terminal 
- run virtual environment by running "./.venv/Scripts/activate" in your terminal 
- install project requirements - run "pip install -r requirements.txt" in your terminal 
- run server "uvicorn app.main:app --reload" in your terminal
- go to "http://127.0.0.1:8000" or "localhost:8000" in your browser, add different expenses, see the chart and table update and delete expenses. 
