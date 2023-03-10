from django.shortcuts import render
import environ
import requests
import os
from ta_metrics_project.settings import CF_API
from datetime import datetime, timedelta
import json


# Create your views here.
def call_api(start_date, end_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    num_of_days = datetime.now() - start_date

    base_url = CF_API
    url = base_url + str(num_of_days.days)

    res = requests.get(url)

    container = create_container(start_date, end_date, res.json())

    #return res.json()
    return json.dumps(container)


def create_container(start, end, data):
    start_date = datetime.date(start)
    end_date = datetime.date(end)

    delta = end_date - start_date

    container = []

    for i in range(delta.days + 1):
        cur_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        day = {cur_date: {'1-2 PM': {"tickets": None, "waittime": None},
                          '2-3 PM': {"tickets": None, "waittime": None},
                          '3-4 PM': {"tickets": None, "waittime": None},
                          '4-5 PM': {"tickets": None, "waittime": None},
                          '5-6 PM': {"tickets": None, "waittime": None},
                          '6-7 PM': {"tickets": None, "waittime": None},
                          '7-8 PM': {"tickets": None, "waittime": None},
                          '8-9 PM': {"tickets": None, "waittime": None},
                          '9-10 PM': {"tickets": None, "waittime": None}
                          }
               }

        container.append(day)

    return container


if __name__ == "__main__":
    print(call_api(1))
