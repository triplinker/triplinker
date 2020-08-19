# TripLinker :octocat:

[![Build Status](https://travis-ci.org/triplinker/triplinker.svg?branch=master)](https://travis-ci.org/github/triplinker/triplinker)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/triplinker/triplinker/blob/master/LICENSE)

---

## Getting Started

These instructions will help you to get the copy of the project for development and testing purposes.

## Running Locally

### Clone the project to your local machine

```
git clone https://github.com/triplinker/triplinker
```

### Install poetry  

```
pip install poetry
```

### Install all dependencies

***Note:*** before that you need to get to the directory with the project, then you can write the command below: 

```
poetry install
```

### Create .env file near the manage.py file 

***Note:*** .env will be invisible, so make it visible and set the following values inside: 

```
DEBUG=on
SECRET_KEY="dev"
DATABASE_URL=psql://test:test@127.0.0.1:5432/test
STATIC_URL=/static/
```

If you are using another DB for development then check the [documentation](https://django-environ.readthedocs.io/en/latest/) out for more information. 
### Create database

```
sudo -u postgres psql
```

Enter the password and then write:

```
CREATE DATABASE test;
```

### Create user in the DB 

```
CREATE USER test with encrypted password 'test';
```

Done! We have created a new user with the name "test" and password "test".

### Make migrations

```
python manage.py makemigrations 
```

After this:

```
python manage.py migrate
```

### Create superuser

```
python manage.py createsuperuser
```

#### Example:

```
E-mail: your@email.com
First name: Name
Second name: Surname
Sex: M
Date of birth: 2000-10-12
Country: BY
Password: secret
```

***Note:***

```
Sex: M
```

**M** means **Male**.
For example, if you write **F** here, then it will mean **Female**.

```
Country: BY
```

**BY** means **Belarus**. That's just the Alpha-2 code for the country.

### Run Celery

Some applications in our project needs Celery, so before you run the server please write this command:
```
celery -A core worker --loglevel=info

```

### Run server

***Note:*** make sure that you're in the same directory where the file manage.py is located.

```
python manage.py runserver
```
## Running the tests

When you get to the directory 'triplinker/triplinker' just run the command:

```
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/triplinker/triplinker/blob/master/LICENSE) file for details.
