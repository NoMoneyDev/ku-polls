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
Activate your virtual environment
```
venv/Script/activate
```
Install the required packages
```
pip install -r requirements.txt
```
Initailize Database
```
python ./manage.py migrate
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
Activate your virtual environment
```
source venv/bin/activate
```

Initailize Database
```
python manage.py migrate
```

## Setup your .env
1. Create a file called `.env` in ku-polls directory
2. Copy contents of `sample.env` to `.env`
3. Use the following command to generate your `SECRET_KEY`
```
python manage.py shell -c "from django.core.management import utils; print(utils.get_random_secret_key())"
```
4. Configure your `.env` to fit your usage
- DEBUG: True / False
- ALLOWED_HOSTS: should be in **EXACTLY** this format
```
ALLOWED_HOSTS =localhost, your-host-here, another-host-here
```
- TIME_ZONE: Look up your **timezone identifier** [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)

## Loading data
Load data you want using this command. Replace `data-you-want-to-load` with the filename of your data
```
python manage.py loaddata data/data-you-want-to-load
```