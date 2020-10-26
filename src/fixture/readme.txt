--- 1.Rebuild f1app.json -----------------------------------------------------
# in the f1\fixture directory:
### four input CSV files: (Note: For the CSV files, do not leave any blank space ' ' !!!)
    employee.csv
    country.csv
    agent.csv
    dependent.csv

# run the following Python command to generate the output JSON file: f1app.json

python json4csv.py



--- 2. Rebuild db.sqlite3-----------------------------------------------------
# copy f1app.json in the fixture directory to the f1 directory
# move to the f1 directory

# remove the old database models
del db.sqlite3

# initialize Django models:
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata f1app.json



--- 3. Ready to start server--------------------------------------------------
python manage.py runserver