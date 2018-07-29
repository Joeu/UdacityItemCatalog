# Udacity Item (Games) Catalog

A web application built with Flask (Python library) with authentication and authorization features.

## Getting Started

The following instructions will get you a copy of the project and will set you up to run on your local machine.

### Prerequisites

You will need to have Python

```
Python 2.7.12
```

The following Python libraries

```
bleach==2.1.1
certifi==2017.11.5
chardet==3.0.4
click==6.7
Flask==0.9
Flask-HTTPAuth==3.2.3
Flask-Login==0.1.3
Flask-SQLAlchemy==2.3.2
html5lib==1.0b10
httplib2==0.10.3
idna==2.6
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
oauth2client==4.1.2
packaging==16.8
passlib==1.7.1
psycopg2==2.7.3.2
pyasn1==0.3.7
pyasn1-modules==0.1.5
pyparsing==2.2.0
redis==2.10.6
requests==2.18.4
rsa==3.4.2
six==1.11.0
SQLAlchemy==1.1.15
urllib3==1.22
webencodings==0.5.1
Werkzeug==0.8.3
```
And a browser of your choice.

And also the database file from Udacity

## Installation

>Clone the repository and move to the project folder:

    $ git clone https://github.com/Joeu/Udacity_Report_Tool

>Go to the project root directory and run:

    $ pip install package

## Application setup

After the package installation, you need to run the following commands in sequence to create and populate the database

>Go to the project root directory and run:

    $ python database_setup.py
    $ python gamerecords.py

## Running the application locally

>Still in the project root directory and run:

    $ python catalog.py

### Using the application

>With a browser of your choice, access:

    localhost:5000


* The catalog is ready to be used.
