# Yatube Web-blog

## Description

It's a blog where you can post your thoughts and opinions about different subjects.
You are able to choose a specific **group** for your post.
Also you can follow another authors and view posts from followed people.

## Installation

1. clone repository and enable virtual environment
For Windows:
```
python -m venv venv
./venv/Scripts/activate.bin
```
For Linux:
```
python3 -m venv venv
. /venv/Scripts/activate
```
2. Install requirements
```
pip install -r requirements.txt
```
3. Make and run migrations
```
python manage.py makemigrations
python manage.py migrate
```
4. Collect static
```
python manage.py collectstatic
```
5. Run server
```
python manage.py runserver
```

## Technology-Stack

1. Python 3.7
2. Django 2.2
