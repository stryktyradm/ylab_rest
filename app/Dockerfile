FROM python:3.10.1-slim

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/

RUN bash -c "pip install -r requirements.txt"

COPY . /app/

RUN bash -c "chmod +x prestart.sh"

RUN bash -c "chmod +x test-start.sh"

ENV PYTHONPATH=.
