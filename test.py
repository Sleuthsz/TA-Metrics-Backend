from ta_metrics.views import call_api, convert_to_pacific_time, get_tickets_and_wait, create_container
from datetime import datetime, timedelta
import pytz

# create_time = datetime.strptime("2023-03-06T19:56:51.192Z", '%Y-%m-%dT%H:%M:%S.%fZ')
    # assigned_time = datetime.strptime("2023-03-06T21:04:47.649Z", '%Y-%m-%dT%H:%M:%S.%fZ')
    #
    #
    #
    # # date_str = '2023-03-09T03:43:10.508Z'
    # # date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

if __name__ == "__main__":
    #print(call_api('2023-02-27', '2023-03-03'))
    #
    # start_date = datetime.strptime('2023-02-27', '%Y-%m-%d')
    # end_date = datetime.strptime('2023-03-03', '%Y-%m-%d')
    #
    # num_of_days = datetime.now() - start_date
    #
    # print(num_of_days)

    # new_timezone = pytz.timezone('US/Pacific')
    # time = datetime.strptime("2023-03-06T21:04:47.649Z", '%Y-%m-%dT%H:%M:%S.%fZ')
    #
    # print(time.replace(tzinfo=pytz.utc).astimezone(new_timezone))

    # start_date = datetime.strptime('2023-02-27', '%Y-%m-%d')
    # start_date = start_date + timedelta(days=1)
    # print(start_date)

    # print(call_api('2023-03-06', '2023-03-08'))

    print(get_tickets_and_wait('2023-03-06', '2023-03-09'))


    #print(create_container('2023-02-27', '2023-03-03'))


