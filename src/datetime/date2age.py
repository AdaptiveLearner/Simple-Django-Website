from datetime import date

your_date_string = '1975/01/02'
year, month, day = [int(s) for s in your_date_string.split('/')]

today = date.today()
print (today.year - year - ((today.month, today.day) < (month, day)))