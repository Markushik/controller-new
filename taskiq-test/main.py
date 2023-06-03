from datetime import datetime

date_str = '09-19-2022'

date_object = datetime.strptime(date_str, '%m-%d-%Y').date()

print(date_object, type(date_object))