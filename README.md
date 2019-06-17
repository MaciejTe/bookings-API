[![Build Status](https://travis-ci.com/MaciejTe/bookings-API.svg?branch=master)](https://travis-ci.com/MaciejTe/bookings-API) 
[![Coverage Status](https://coveralls.io/repos/github/MaciejTe/bookings-API/badge.svg?branch=master)](https://coveralls.io/github/MaciejTe/bookings-API?branch=master)
[![Coverage Status](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Bookings REST API
--------------


REST API for booking purposes.

[Changelog](CHANGELOG.md)

### Documentation
Documentation is available after launching application in development mode by isuing following command:

```flask run```

Swagger docs are available here (assuming application is run inside Docker at localhost):

```http://127.0.0.1:5000/```

### Development
In order to launch development environment, Docker image needs to be built:

```docker build -t bookings_api .```

After building image, container can be run (following command assumes current working directory is main repository directory):

```docker run --network host -w /booking_api -it --rm -v "${CWD}":/booking_api/ bookings_api bash```

Inside container, setup.py needs to be launched in develop mode:

```python setup.py develop```
