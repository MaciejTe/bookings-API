###################################################
## Development purposes Dockerfile
###################################################

FROM python:3.6.3

COPY . /bookings_api
WORKDIR /bookings_api

ENV FLASK_DEBUG 1
ENV FLASK_APP bookings_api.py

RUN pip install --upgrade pip

RUN python setup.py install
