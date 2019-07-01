from faker import Faker
from datetime import datetime

fake_obj = None


def get_faker():
    global fake_obj
    if fake_obj is None:
        fake_obj = Faker()
    return fake_obj


fake: Faker = get_faker()


def get_fake_datetime(start=datetime(2018, 1, 1, 0, 0, 0), end=datetime(2018, 12, 31, 23, 59, 59)):
    return fake.date_time_between_dates(datetime_start=start, datetime_end=end)
