import datetime
from dateutil.parser import parse

# tday = datetime.date.today()
# tdelta = datetime.timedelta(days=2)
# date = tday + tdelta
# print(date)
# month = date.strftime("%B")
# years = date.strftime("%Y")
# weekday = date.strftime("%A")
# date = date.strftime("%d")
# expected_delivery_date = weekday + ' ' + date + ' ' + month + ' ' + years

# print(expected_delivery_date)
# # a=datetime.datetime.strptime(expected_delivery_date, "%Y/%m/%d %H:%M:%S.%f")
# # print('aaaa',a)

a = 'Wednesday 15 June 2022'
dt = parse(a)
z=dt.date()
print(z.isoformat())
tday = datetime.date.today()
print(tday)
p=z-tday
print(p.days)