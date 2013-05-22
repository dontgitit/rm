import datetime
import time

from dateutil.relativedelta import relativedelta

DATE_FORMAT = '%Y-%m-%d'

# http://stackoverflow.com/questions/4039879/best-way-to-find-the-months-between-two-dates-in-python
def diff_month(d1, d2):
    return (d1.year - d2.year)*12 + d1.month - d2.month

# the following two functions assume each period is a month
# TODO: make period length dynamic

# convert a python datetime or string into a "period" index for the RSR model
def date2period(date, first_dt):
    dt = date
    if not isinstance(dt, datetime.datetime):
        dt = datetime.datetime.strptime(date, DATE_FORMAT)
    return diff_month(dt, first_dt)

# converts a python datetime into utc milliseconds for flotjs
def period2jsdate(period, first_dt):
    return int(time.mktime((first_dt + relativedelta(months=+period)).timetuple())) * 1000
