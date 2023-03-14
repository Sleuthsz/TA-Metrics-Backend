from django.shortcuts import render
import environ
import requests
import os
from ta_metrics_project.settings import CF_API
from datetime import datetime, timedelta
import json
import pytz
from django.http import JsonResponse
import multiprocessing as mp
from multiprocessing import pool
from dateutil import parser
import numpy as np
from .view_helpers.api_call import call_api, get_request
from .view_helpers.daily_helpers import fields_to_pacific_dates, pop_day_container, get_hour_str, to_pacific_time, create_day_container


def daily_tickets_waits(request):
    """
    Populates container with data on number of tickets and total wait times
    """
    start_date, end_date = get_request(request)

    data = call_api(start_date)
    container = create_day_container(start_date, end_date)

    start_date = start_date.replace(tzinfo=pytz.timezone('US/Pacific'))

    for day in data:
        # Discard entries with null values
        if any(key not in day or not day[key] for key in ['createTime', 'assignedTime', 'completeTime']):
            continue

        try:
            day = fields_to_pacific_dates(day)
        except ValueError:
            continue

        date_idx = (day['createTime'] - start_date).days

        if date_idx < len(container):
            pop_day_container(container, day, date_idx)

    return JsonResponse(container, safe=False)


def get_summary_stats(request):
    """
    Returns summary statistics on wait times for a range of dates
    """
    start_date, end_date = get_request(request)

    data = call_api(start_date)

    date_list = []

    for item in data:
        if 'createTime' in item and item['createTime'] and 'assignedTime' in item and item['assignedTime']:
            assigned = parser.parse(item['assignedTime']).timestamp()
            created = parser.parse(item['createTime']).timestamp()
            if start_date.timestamp() <= assigned <= end_date.timestamp():
                date_list.append(assigned - created)

    date_array = np.array(date_list)

    with mp.Pool() as pool:
        mean_date = np.mean(date_array)
        median_date = np.median(date_array)
        avg_time_delta = np.mean(np.abs(date_array - mean_date))

    summary_data = {'mean': mean_date, 'median': median_date, 'average_time_delta': avg_time_delta}

    return JsonResponse(summary_data, safe=False)
