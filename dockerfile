FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN apk update && apk add bash

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

