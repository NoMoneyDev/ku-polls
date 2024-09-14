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

## Loading data
Load data you want using this command. Replace `data-you-want-to-load` with the filename of your data
```
python manage.py loaddata data/data-you-want-to-load
```