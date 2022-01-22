FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN apk update && apk add bash

RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

