FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN apk update && apk add bash

RUN pip install --upgrade pip

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

