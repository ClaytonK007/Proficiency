# To-Do list

## Requirements

- allow a task to be added
- toggle a task to mark it as completed
- allow a task to be deleted
- PostGreSQL database

## How to deploy and test:
- download or pull project repository
- create a virtual environment in the repository - run "python -m venv .venv" in your terminal 
- run virtual environment by running "./.venv/Scripts/activate" in your terminal 
- install project requirements - run "pip install -r requirements.txt" in your terminal 
- run server "uvicorn app.main:app --reload" in your terminal
- go to "http://127.0.0.1:8000" or "localhost:8000" in your browser and create a task, toggle it and delete.
