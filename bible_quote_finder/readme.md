# Bible quote finder

## Requirements

- Allow user to find a verse in the Bible based on a topic or keyword they input
- allow a favourite quote to be added and deleted

## How to deploy and test:
- download or pull project repository
- create a virtual environment in the repository - run "python -m venv .venv" in your terminal 
- run virtual environment by running "./.venv/Scripts/activate" in your terminal 
- install project requirements - run "pip install -r requirements.txt" in your terminal 
- run server "uvicorn app.main:app --reload" in your terminal
- go to "http://127.0.0.1:8000" or "localhost:8000" in your browser, find a quote based on a topic or keyword, add a favourite and delete a quote. 
