# Sikre

**Please note:** *Sikre is in early development stages, it's not recommended to use it in production yet.*

Sikre is a high-security backend API to store your passwords and sensitive data
securely (like SSH keys and SSL certificates).

It's made with paranoid security in mind, that means the server will never know
anything about the data you uploaded, it's going to get encrypted so there is
no way for the person managing the instance or the server itself to decrypt or
read your information.

This is just the backend part, so unless you are \<insert genius name here\> you
will probably need a frontend to work with. You can use the default
[sikre-frontend](https://github.com/clione/sikre-frontend) project.

## What does it use?

* [Falcon microframework](http://falconframework.org/)
* [Talons (Falcon auth)](https://pypi.python.org/pypi/talons/0.1)
* [Peewee ORM](http://peewee.readthedocs.org/en/latest/)

## Requirements

* A GNU/Linux server
* Python 3.4+
* A valid SSL certificate

Please note that this project **won't run** on Python 2.7.x series.

## How to install

To install please follow these steps:

* Install a virtual environment

    `$ pyvenv <folder name>`

* Activate the environment

    `$ source <virtualenv folder>/bin/activate`

* Install the dependencies

    `$ pip install requirements.txt`

That will install Falcon and the required dependencies for the rest of the
project.

## How to run

As a included dependency, and for the sake of separating components as most
as we are able, we included *uwsgi* in the dependencies, so you can test run
your project with the following command (inside the virtual environment):

`$ uwsgi --http :8080 --wsgi-file app.py --callable api`

Now you can visit your application going to `localhost:8080` in your browser.
Please remember that this is the backend, so it will only reply to the API
endpoints, you will not be able to see anything else.

There is a test endpoint while in debug mode which you can visit in:
`localhost:8080/test_api`
