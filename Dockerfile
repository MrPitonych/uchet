FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN mkdir /app
COPY ./app /app
COPY ./requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt

