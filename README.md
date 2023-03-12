# TA Metrics

## Team Members

**Daniel Brott**

**Monika Davies**

**Alejandro Rivera**

**Andy Nguyen**

**Natalija Germek**

## Project Description

This project is a full-stack application which aims to help Code Fellows administrators and teaching assistants (TAs) visualize metrics regarding help ticket velocity (how many help tickets each TA is taking everyday, how long is each TA spending on a ticket, which classes have the most number of tickets at any given time, etc.). Through this project, Code Fellows administrators are able to identify how to best allocate TAs to help students as well as identify possible areas of improvement with Code Fellows' course curriculums.

## Tools Used

- Trello
- PyCharm
- Django
- Python
- NextJS
- React
- JavaScript

## Links and Models

- [Trello](https://trello.com/b/jz4OJzfn/ta-metrics)

- [Domain Model](documentation/domain_model.png)

## Functions and Methods

| Function or Method        | Summary | Big O Time | Big O Space | Example                       | 
|:--------------------------| :----------- |:----------:|:-----------:|:------------------------------|
| call_api()                | Makes call to Code Fellows API and returns JSON data from specified start date |    O(1)    |    O(1)     | call_api(start_date)          |
| get_tickets_and_wait()    | Populates container with data on number of tickets and total wait times |    O(n)    |    O(1)     | get_tickets_and_wait(request) |
| get_hour_window()         | Converts hour to string for dictionary look up in container |    O(n)    |    O(1)     | get_hour_window(time)         |
| convert_to_pacific_time() | Converts datetime objects from Code Fellows API to Pacific timezone |     O      |      O      | convert_to_pacific_time(time) |
| create_container() | Creates empty container for get_tickets_and_wait function |     O      |      O      | create_container(start, end)  |



## Change log

- Crated Wireframes, Domain Model, updated README.md - 07 March 2023. - Updated README.md

### Version

*Version 1.0* Created team agreement, Trello board, README - March 6, 2023

*Version 1.1* Continued to completed call_api() function - 08 March 2023

*Version 2.0* Refactor API call functions. Refactor date/time function to access date based on client date range input. - 09 March 2023

*Version 2.1* Completed Functions for API calculation and data gathering, updated README.md. - 11 Mar 2023