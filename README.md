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
Flask
SQLAlchemy
```
And a browser of your choice.

## Installation

>Clone the repository and move to the project folder:

    $ git clone https://github.com/Joeu/UdacityItemCatalog

>Go to the project root directory and run:

    $ sudo pip install flask
    $ sudo pip install sqlalchemy

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

    http://localhost:5000


* The catalog is ready to be used.
