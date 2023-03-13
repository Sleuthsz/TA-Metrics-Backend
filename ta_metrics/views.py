from django.shortcuts import render
import environ
import requests
import os
from ta_metrics_project.settings import CF_API
from datetime import datetime, timedelta
import json
import pytz
# from django.http import HTTPRequest, HttpResponse
from django.http import JsonResponse
import multiprocessing as mp
from multiprocessing import pool
from dateutil import parser
import numpy as np


# Create your views here.
def call_api(start_date):
    """
    Makes call to Code Fellows API and returns JSON data from specified start date
    """
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    if start_date > datetime.now():
        raise Exception('Invalid Date')

    num_of_days = datetime.now() - start_date

    base_url = CF_API
    url = base_url + str(num_of_days.days)

    res = requests.get(url)

    return res.json()


def get_tickets_and_wait(request):
    """
    Populates container with data on number of tickets and total wait times
    """
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    data = call_api(start_date)

    container = create_container(start_date, end_date)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    count = 0

    for day in data:

        # Discard entries with null values
        if 'createTime' not in day or 'assignedTime' not in day or 'completeTime' not in day:
            continue

        if not day['createTime'] or not day['assignedTime'] or not day['completeTime']:
            continue

        try:
            # Convert all dates/times to Pacific timezone
            day['createTime'] = convert_to_pacific_time(day['createTime'])
            day['assignedTime'] = convert_to_pacific_time(day['assignedTime'])
            day['completeTime'] = convert_to_pacific_time(day['completeTime'])
        except ValueError as e:
            count += 1
            continue

        start_date = start_date.replace(tzinfo=pytz.timezone('US/Pacific'))

        date_idx = day['createTime'] - start_date
        date_idx = date_idx.days

        if date_idx < len(container):
            wait_time = day['assignedTime'] - day['createTime']
            wait_time = int(wait_time.total_seconds())

            hour_window = get_hour_window(day['createTime'])

            container[date_idx]['hours'][hour_window]['tickets'] += 1
            container[date_idx]['hours'][hour_window]['tot_wait'] += wait_time

    # return json.dumps(container)
    return JsonResponse(container, safe=False)


def get_hour_window(time):
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

    # return data[0]


def convert_to_pacific_time(time):
    """
    Converts datetime objects from Code Fellows API to Pacific timezone
    """
    new_timezone = pytz.timezone('US/Pacific')
    time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
    return time.replace(tzinfo=pytz.utc).astimezone(new_timezone)


def create_container(start, end):
    """
    Creates empty container for get_tickets_and_wait function
    """
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    delta = end_date - start_date

    container = []

    for i in range(delta.days + 1):
        cur_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        day = {'date': cur_date,
               'hours': {'7 AM': {'tickets': 0, 'tot_wait': 0},
                         '8 AM': {'tickets': 0, 'tot_wait': 0},
                         '9 AM': {'tickets': 0, 'tot_wait': 0},
                         '10 AM': {'tickets': 0, 'tot_wait': 0},
                         '11 AM': {'tickets': 0, 'tot_wait': 0},
                         '12 PM': {'tickets': 0, 'tot_wait': 0},
                         '1 PM': {'tickets': 0, 'tot_wait': 0},
                         '2 PM': {'tickets': 0, 'tot_wait': 0},
                         '3 PM': {'tickets': 0, 'tot_wait': 0},
                         '4 PM': {'tickets': 0, 'tot_wait': 0},
                         '5 PM': {'tickets': 0, 'tot_wait': 0},
                         '6 PM': {'tickets': 0, 'tot_wait': 0},
                         '7 PM': {'tickets': 0, 'tot_wait': 0},
                         '8 PM': {'tickets': 0, 'tot_wait': 0},
                         '9 PM': {'tickets': 0, 'tot_wait': 0},
                         '10 PM': {'tickets': 0, 'tot_wait': 0},
                         }
               }

        container.append(day)

    return container


def get_summary_stats():
    # start_date = request.GET.get('start_date')
    # end_date = request.GET.get('end_date')

    start_date = '2023-03-08'


    data = call_api(start_date)

    date_list: list[float] = []

    for item in data:
        if 'createTime' in item and item['createTime'] and 'assignedTime' in item and item['assignedTime']:
            assigned = parser.parse(item['assignedTime']).timestamp()
            created = parser.parse(item['createTime']).timestamp()
            date_list.append(assigned - created)

    #date_array: np.ndarray = np.array([parser.parse(date).timestamp() for date in date_list])
    date_array: np.nparray = np.array(date_list)
    with mp.Pool() as pool:
        mean_date: float = np.mean(date_array)
        median_date: float = np.median(date_array)
        avg_time_delta: float = np.mean(np.abs(date_array - mean_date))

    return {'mean': mean_date, 'median': median_date, 'average_time_delta': avg_time_delta}
