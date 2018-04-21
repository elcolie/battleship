# Battleship
A famouse board game. This is backned API for a Battleship clone

# Requirements
1. `postgres 10`
1. `Django2`
1. `python3`

# Installation
1. `CREATE DATABASE "battleshipdb";`
1. `pip install requirements.txt`
1. `python manage.py migrate`
1. `python manage.py collectstatic`
1. `python manage.py runserver`

# Testing
1. `pytest -n #processors -v`

# Miscellaneous
1. Place ship one by one over dedicated endpoint.
 Since I don't know the use case yet.
