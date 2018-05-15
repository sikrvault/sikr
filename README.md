# Sikr

[![Build Status](https://travis-ci.org/sikrvault/sikr.svg?branch=master)](https://travis-ci.org/sikrvault/sikr)
[![Coverage Status](https://coveralls.io/repos/github/sikrvault/sikr/badge.svg?branch=master)](https://coveralls.io/github/sikrvault/sikr?branch=master)
[![Docs Status](https://readthedocs.org/projects/sikre/badge/?version=latest)](http://sikre.rtfd.io/)

**Please note:** *Sikr is in early development stages, it's not recommended to use it in production yet.*

Sikre is a high-security backend API to store your passwords and sensitive data
securely (like SSH keys and SSL certificates).

It's made with paranoid security in mind, that means the server will never know
anything about the data you uploaded, it's going to get encrypted so there is
no way for the person managing the instance or the server itself to decrypt or
read your information.

This is just the backend part, so unless you are \<insert genius name here\> you
will probably need a frontend to work with. You can use the default
[sikr-frontend](https://github.com/sikrvault/sikr-frontend) project.

## Who uses it?

The official password storage service called `Sikr` (as Sikre/Sikr in Danish, to ensure, protect) is going to use it. It's still on development (tied to the project) but you can reach it on http://sikr.io and http://api.sikr.io

## What does it use?

* [Falcon microframework](http://falconframework.org/)
* [Python Requests](http://docs.python-requests.org/en/latest/)
* [PyJWT](https://github.com/jpadilla/pyjwt)
* [SQLAlchemy ORM](http://www.sqlalchemy.org/)

## Requirements

* A GNU/Linux server
* Python >= 3.6 (tested up to 3.7)
* A valid SSL certificate (not necessary if DEBUG=True)

Please note that this project **won't run** on Python 2.7.x series or
Python 3.x below 3.6

## How to install

To install please follow these steps (these instructions use Pipenv, if you
don't know what that is, please check it [here](https://docs.pipenv.org/))

* Install the dependencies

    `$ cd <your_sikr_git_folder>`
    `$ pipenv install`

* Activate the virttual environment

    `$ pipenv shell`

That should install and lock all the necessary requirements. If you're confused
about how pipenv works, let's just say it takes care of the creation, isolation
and activation of the correct virtual environment on its own, you don't need to
do anything.

## How to run

There is two ways of running the application. One is the main wsgi application
that will serve all the requests. The other is running it as a management
script.

### Run as service

To run it for testing you can use gunicorn or uwsgi or any other wsgi
interface. To run it with uwsgi for example:

`$ uwsgi --http :8080 --wsgi-file app.py --callable api`

Now you can visit your application going to `localhost:8080` in your browser.
Please remember that this is the backend, so it will only reply to the API
endpoints, you will not be able to see anything else.

There is a test endpoint while in debug mode which you can visit in:
`localhost:8080/test_api`

### Run as management script

To run the application as a management script you just need to invoke it
from python:

`$ python app.py`

This script contains multiple actions that take care of the service. At
the moment of writing this document these are the functions:

* `syncdb` Creates the database schema necessary to run the application
* `generate` Fills the database with random data. This command only runs if DEBUG=True

## License and copyright

This project is licensed under the MIT license.

## Authors

Oscar Carballal Prego <oscar.carballal@esmorga.eu>
