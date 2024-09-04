# KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

# Requirements
- Django >= 5.1
- python-decouple 

# Installation
## Windows
Clone this repository
```
git clone https://github.com/NoMoneyDev/ku-polls.git
```
Create a virtual environment for the application
```
python -m venv .venv
```
Install the required packages
```
pip install -r requirements.txt
```
Initailize Database
```
python ./manage.py migrate
```
Load sample polls into database
```
python manage.py loaddata data/polls-v1.json
```

## MacOS
Clone this repository
```
git clone https://github.com/NoMoneyDev/ku-polls.git
```
Create a virtual environment for the application
```
python -m venv venv
```
Install the required packages
```
pip install -r requirements.txt
```
Initailize Database
```
python manage.py migrate
```
Load sample polls into database
```
python manage.py loaddata data/polls-v1.json
```

# Running the Application
This command will run the application on localhost:8000
```
python manage.py runserver
```

# Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project%20Plan)

# Test Badge
[![Python application](https://github.com/NoMoneyDev/ku-polls/actions/workflows/python-app.yml/badge.svg)](https://github.com/NoMoneyDev/ku-polls/actions/workflows/python-app.yml)
