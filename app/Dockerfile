FROM python:3.7.6-slim-buster
USER root

# PSQL Requirements
RUN apt-get update && apt-get install -y libpq-dev build-essential libpcre3 libpcre3-dev

# Requirements
ADD requirements.txt .
RUN pip install -r requirements.txt

# User for server
RUN useradd app-server

WORKDIR /usr/local/app

# RUN sleep infinity
