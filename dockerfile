FROM python:3.9-alpine

WORKDIR /usr/src/app

RUN apk update && apk add bash

RUN pip install --upgrade pip

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log  --bind 0.0.0.0:8000"]
# --workers 2 --daemon