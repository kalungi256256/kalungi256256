import calendar

fmonth = input("Enter the first month (e.g. January): ")
year = int(input("Enter the year: "))
actual_date = calendar.month_name.index(fmonth)
prefered_month = calendar.month_name.index(fmonth)
print(calendar.month(prefered_month, year))
