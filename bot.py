#!/bin/python3

import requests
import json
from datetime import datetime, date, time as dt_time, timedelta
import calendar
from time import sleep
from termcolor import colored
from random import randint
import notify2

notify = True

def is_weekend(today):
    try:
        isinstance(today, datetime)
        upper_limit = today + timedelta(days=(6 - today.weekday()))
        lower_limit = today + timedelta(days=(5 - today.weekday()))
        if today >= lower_limit <= upper_limit:
            return True
        else:
            return False
    except ValueError:
        print('Your date is not a datetime object.')

def date_check(date):
    # print("Hour: "+str(date.hour))
    if is_weekend(date):
        if date.hour > 9 and date.hour < 21:
            if notify == True:
                n = notify2.Notification('PadelBot', 'Timeslot on WEEKEND found!')
                n.show()
            return True
    else:
        if date.hour >= 7 and date.hour < 8:
            return True
        elif date.hour >= 17 and date.hour < 20:
            return True
        else:
            return False

if notify == True:
    notify2.init('PadelBot')
format_string = "%Y-%m-%dT%H:%M:%S"

today = date.today()

for i in range(0,30):
    days = 1*i+1
    days_added = timedelta(days = days)

    search_day = datetime(today.year,today.month,today.day) + days_added

    start_time = dt_time(0,0,0)
    end_time = dt_time(23,59,59)

    start_date = datetime(search_day.year, search_day.month, search_day.day, start_time.hour, start_time.minute, start_time.second)
    end_date = datetime(search_day.year, search_day.month, search_day.day, end_time.hour, end_time.minute, end_time.second)

    params = (
        ('user_id', 'me'),
        ('tenant_id', '17a13ee4-2d0c-438e-978e-56efe5ec4948'),
        ('sport_id', 'PADEL'),
        ('local_start_min', start_date.strftime(format_string)),
        ('local_start_max', end_date.strftime(format_string)),
    )

    # response = requests.get('https://playtomic.io/api/v1/availability', headers=headers, params=params)
    response = requests.get('https://playtomic.io/api/v1/availability', params=params)

    courts = response.json()

    weekday = calendar.day_name[search_day.weekday()]
    friendly_date = datetime.strftime(search_day,"(%d/%m/%y)")

    in_format_string = "%H:%M:%S"
    hours = 2
    hours_added = timedelta(hours = hours)

    time_slot_found = False
    for court in courts:
        slots = court["slots"]

        for slot in slots:
            slot_time = datetime.strptime(slot["start_time"], in_format_string) + hours_added
            slot_time = datetime(search_day.year, search_day.month, search_day.day, slot_time.hour, slot_time.minute, slot_time.second)

            if date_check(slot_time):
                time_slot_found = True
                break

    if time_slot_found:
        text = colored("Timeslot found!", "green")
    else:
        text = colored("Fully booked", "red")

    print("{} {}: {}".format(friendly_date, weekday, text))
    
    sleep(randint(1,5))

# print(json.dumps(response.json(), indent=4))

with open('response.txt', 'w') as outfile:
    json.dump(response.json(), outfile, indent=4)

