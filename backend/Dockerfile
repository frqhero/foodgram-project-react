#!/bin/bash
FROM python:3.10.4

WORKDIR /app

COPY backend/requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./ ./

WORKDIR backend

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]