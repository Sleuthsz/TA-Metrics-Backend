from django.shortcuts import render
import environ
import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(dotenv_path)
#env = environ.Env()
# environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../ta_metrics_project/.env'))


# Create your views here.
def call_api(num):
    # base_url = env.str('CF_API')
    base_url = os.environ.get('CF_API')
    url = base_url + str(num)

    res = requests.get(url)

    return res.json()


if __name__ == "__main__":
    print(call_api(1))
