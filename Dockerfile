###################################################
## Development purposes Dockerfile
###################################################

FROM python:3.6.3

COPY /bookings_api /bookings_api

RUN sudo apt install sqlite
RUN pip install --upgrade pip
RUN python setup.py install


