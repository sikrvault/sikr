# Sikre

Sikre is a high-security backend API to store your passwords and sensitive data
securely (like SSH keys and SSL certificates).

It's made with paranoid security in mind, that means the server will never know
anything about the data you uploaded, it's going to get encrypted so there is
no way for the person managing the instance or the server itself to decrypt or
read your information.

This is just the backend part, so unless you are <insert genius name here> you
will probably need a frontend to work with. You can use the default
sikre-frontend project.

## Requirements

* A GNU/Linux server
* Python 3.4+

Please note that this project **won't run** on Python 2.7.x series.

## How to install

To install please follow these steps:

* Install a virtual environment

    $ pyvenv <folder name>

* Activate the environment

    $ source <virtualenv folder>/bin/activate

* Install the dependencies

    $ pip install requirements.txt

That will install Falcon and the required dependencies for the rest of the
project

