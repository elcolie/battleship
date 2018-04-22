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

# Prerequisite
1. `python manage.py createsuperuser`   To create `admin` user
1. `admin` logins to `http://localhost:8000/admin/` to add `john` as a new user


# Testing
1. `coverage run --source fleets/ -m py.test .` # Prepare coverage
1. `coverage report` # Brief report
1. `coverage html`  # To see html coverage

# How to play
1. One player create `board`.
    ```
    Method: `POST`
    URL: `http://localhost:8000/api/boards/
    Payload:
    {
        'defender': <user1_id>,
        'attacker': <user2_id>,
    }
    Response:
    {
        "id": 2,
        "defender": 1,
        "attacker": 2,
        "is_done": false
    }
    ```
`"id": 2` is a `board_id`

1. Suppose `john` plays as a `defender`. He places the horizontal battleship and top-left.
And also placing the rest of the fleet. Coordinate index start from left to right, up to down
    ```
    Method: `POST`
    URL: `http://localhost:8000/api/fleets/
    Payload:
    {
        'board': 2,
        'fleet_type': "battleship",
        'vertical': false,
        'x_axis': 1,
        'y_axis': 1
    }
    Response:
    {
        "id": 1,
        "board": 2,
        "fleet_type": "battleship",
        "vertical": true,
        "x_axis": 1,
        "y_axis": 1
    }
    ```
*CAUTIONS*: Be careful when you place your fleet. Once you place it. You can not relocate them in the battlefield.

1. `attacker` shooting the missiles to the `defender`'s fleet.
Here is the example of shooting the missile at coordinate (1,1)
And hit the target.
    ```
    Method: `POST`
    URL: `http://localhost:8000/api/missiles/
    Payload:
    {
        'board': 2,
        'x_axis': 1,
        'y_axis': 1,
    }
    Response:
    {
        "message": "Hit"
    }
    ```
Enjoy!
