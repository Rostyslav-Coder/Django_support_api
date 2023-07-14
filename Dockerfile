FROM python:3.11-slim

WORKDIR /app/
COPY . .

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install pipenv

RUN pipenv sync --dev --system

CMD bash
