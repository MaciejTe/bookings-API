###################################################
## Development purposes Dockerfile
###################################################

FROM python:3.9.13

COPY . /bookings_api
WORKDIR /bookings_api

ENV FLASK_DEBUG 1
ENV FLASK_APP bookings_api.py

RUN pip install --upgrade pip

RUN python setup.py install

RUN touch /var/log/cron.log
RUN apt update; apt install -y cron
RUN service cron start
