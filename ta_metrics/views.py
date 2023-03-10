from django.shortcuts import render
import environ
import requests
import os
from ta_metrics_project.settings import CF_API


# Create your views here.
def call_api(num):
    base_url = CF_API
    url = base_url + str(num)

    res = requests.get(url)

    return res.json()


if __name__ == "__main__":
    print(call_api(1))
