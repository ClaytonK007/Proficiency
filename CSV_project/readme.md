# Proficiency Test

2. Manipulating arrays and file handling

## Requirements'

- Make a CSV file of variable length, a form will ask for the amount of data to generate.
- File that is created must have the following headers: Id, Name, Surname, Initials, Age, DateOfBirth
- Import the file into a database and output a count of all the records imported.
- Create two arrays, one for names and one for surnames. There should be 20 Names and 20 Surnames in each array. Use these arrays to generate random names, ages & birthdates to populate a CSV file. The initials are the first character of the name always. Write a function to perform the task of creating the CSV file, you should pass it the number of variations you need.
- The CSV file should be outputted to an output folder, the name of the file must be output.csv.
- An input field will take the amount of records to be generated.
- There should be NO DUPLICATE ROWS IN THE CSV. I.e. The name, surname, age, date of birth must be unique.
- Output a CSV file of 1 000 000 records.
- Import the file using a form variable of file type. One should browse for the file and upload it to the website.
- Create a table called “csv_import” with the relevant fields and types to hold the data of the CSV file. Use code to create the table.

## How to deploy and test:
- download or pull project repository
- create a virtual environment in the repository - run "python -m venv .venv" in your terminal 
- run virtual environment by running "./.venv/Scripts/activate" in your terminal 
- install project requirements - run "pip install -r requirements.txt" in your terminal 
- run server "python app.py" in your terminal
- go to "http://127.0.0.1:8000" or "localhost:8000" in your browser and create a file and then upload it to get the record count.
