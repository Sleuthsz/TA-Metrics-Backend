from django.shortcuts import render
import environ
import requests
import os
from ta_metrics_project.settings import CF_API
from datetime import datetime, timedelta
import json
from django.http import JsonResponse

def call_api(start_date):
    """
    Makes call to Code Fellows API and returns JSON data from specified start date
    """
    if start_date > datetime.now():
        raise ValueError('Invalid Date')

    num_of_days = datetime.now() - start_date

    base_url = CF_API
    url = base_url + str(num_of_days.days)

    res = requests.get(url)

    return res.json()


def get_request(request):
    """
    Gets start and end date query parameters and converts them to datetime objects
    """
    start_date = datetime.strptime(request.GET.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.GET.get('end_date'), '%Y-%m-%d')
    return start_date, end_date