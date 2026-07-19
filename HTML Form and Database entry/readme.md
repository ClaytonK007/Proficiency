# Proficiency Test

1. HTML form with input fields which save to a database

## Requirements:
- Name, Surname, Id No, Date of Birth, POST button, CANCEL button
- validation : id number field only 13 characters long
- validation : date of birth field dd/mm/YYYY format and corresponds to ID number
- validation : valid name and surname
- validation : prompt user if entry already exists
- prompt user if incorrect name or surname is used and prompt if ID number already exists.

## How to deploy and test:
- download or pull project repository
- create a virtual environment in the repository - run "python -m venv .venv" in your terminal 
- run virtual environment by running "./.venv/Scripts/activate" in your terminal 
- install project requirements - run "pip install -r requirements.txt" in your terminal 
- run server "uvicorn api:app --reload"
- go to "http://127.0.0.1:8000" or "localhost:8000" in your browser and add an entry.
- to check if entry is saved in database go to "http://127.0.0.1:8000/docs" or "localhost:8000/docs" in your browser.
    - click on the down arrow by the "Get all users" get method.
    - click on "try it out" button and then click on "execute" button.
    - if successful, it will return a 200 success reponse and display the entry in the response body.

 Alternatively, download a client like DB Browser and open the db file to test in the form was submitted succesfully.
