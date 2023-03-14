from django.shortcuts import render
import environ
import requests
import os
from datetime import datetime, timedelta
import json
import pytz
from django.http import JsonResponse


def fields_to_pacific_dates(day):
    """
    Takes single ticket entry JSON data from Code Fellows API and converts date string fields to datetime objects in Pacific timezone
    """
    day['createTime'] = to_pacific_time(day['createTime'])
    day['assignedTime'] = to_pacific_time(day['assignedTime'])
    day['completeTime'] = to_pacific_time(day['completeTime'])
    return day


def pop_day_container(container, day, date_idx):
    """
    Populates day container
    """
    wait_time = day['assignedTime'] - day['createTime']
    wait_time = int(wait_time.total_seconds())

    hour_window = get_hour_str(day['createTime'])

    container[date_idx]['hours'][hour_window]['tickets'] += 1
    container[date_idx]['hours'][hour_window]['tot_wait'] += wait_time


def get_hour_str(time):
    """
    Converts hour to string for dictionary look up in container
    """
    hour = time.hour

    if hour < 12:
        return str(hour) + ' AM'
    elif hour == 12:
        return str(hour) + ' PM'
    else:
        return str(hour - 12) + ' PM'


def to_pacific_time(time):
    """
    Converts string to datetime object in Pacific timezone
    """
    new_timezone = pytz.timezone('US/Pacific')
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    return time.replace(tzinfo=pytz.utc).astimezone(new_timezone)


def create_day_container(start_date, end_date):
    """
    Creates empty container for get_tickets_and_wait function
    """

    delta = end_date - start_date
    hours = ['7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM',
             '8 PM', '9 PM', '10 PM']

    container = [{'date': (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                  'hours': {hour: {'tickets': 0, 'tot_wait': 0} for hour in hours}}
                 for i in range(delta.days + 1)]

    return container
