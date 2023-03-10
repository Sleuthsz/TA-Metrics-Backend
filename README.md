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

## Setup

Install `mkcert` to self-sign certificates and run HTTPS locally: https://github.com/FiloSottile/mkcert

Run `mkcert -install` to install local certificate authority

Then, in the root of the project, run the following command to generate a certificate:

```bash
mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1
```

Create a `.env` file in the `ta_metrics_project` directory with the following variables:

```dotenv
SLACK_CLIENT_ID=<YOUR_SLACK_CLIENT_ID>
SLACK_CLIENT_SECRET=<YOUR_SLACK_CLIENT_SECRET>
SLACK_REDIRECT_URL=<YOUR_SLACK_REDIRECT_URL>
```

To create a local virtual environment in the root of the project:

```bash
python -m venv .venv
```

To activate the virtual environment:

```bash
source .venv/bin/activate
```

To deactivate the virtual environment:

```bash
deactivate
```

To install dependencies:

```bash
pip install -r requirements.txt
```

To run locally with https:

```bash
python manage.py runserver_plus --cert-file cert.pem --key-file key.pem
```

Reference: https://timonweb.com/django/https-django-development-server-ssl-certificate/

## Change log

- Crated Wireframes, Domain Model, updated README.md - 07 March 2023

### V 1.0

- Created team agreement, Trello board, README - March 6, 2023
