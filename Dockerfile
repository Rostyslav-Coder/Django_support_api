FROM python:3.11-slim

WORKDIR /app/
COPY . .

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install pipenv \
    && pip install watchdog

RUN pipenv sync

CMD python src/manage.py runserver 0.0.0.0:8000
