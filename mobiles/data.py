import datetime

tday = datetime.date.today()
tdelta = datetime.timedelta(days=2)
date = tday + tdelta
month = date.strftime("%B")
years = date.strftime("%Y")
weekday = date.strftime("%A")
date = date.strftime("%d")
expected_delivery_date = weekday + ' ' + date + ' ' + month + ' ' + years
