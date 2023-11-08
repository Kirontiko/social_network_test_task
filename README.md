# Social Network Service

## Table of Contents
 1. [Introduction](#introduction)
 2. [Requirements](#requirements)
 3. [Installation](#installation)
 4. [Used technologies](#used-technologies)
 5. [Endpoints](#endpoints)


## Introduction
Social Network api is providing functionality for users to create a posts,
liking/unliking them, inspect user activity and analytics of posts by certain range of dates.


## Requirements
* python >= 3.9
* pip


## Installation
1. Clone this repository:

    ```
    git clone https://github.com/Kirontiko/social_network_test_task.git
    ```
   
2. Create virtual environment and activate it:
   * Tooltip for windows:
     - ```python -m venv venv``` 
     - ```venv\Scripts\activate```
   * Tooltip for mac:
     - ```python -m venv venv```
     - ```source venv/bin/activate```

3. Install dependencies:
    - ```pip install -r requirements.txt```
4. Apply all migrations in database:
   - ```python manage.py migrate```
5. Run server
   - ```python manage.py runserver```
### App will be available at: ```127.0.0.1:8000```

## Used technologies
    - Django framework
    - Django Rest Framework
    - SQLite


## Endpoints
    "posts": "http://127.0.0.1:8000/api/post/posts",
    "like post": "http://127.0.0.1:8000/api/post/posts/<int:pk>/like",
    "unlike post": "http://127.0.0.1:8000/api/post/posts/<int:pk>/unlike",
    "analytics" : "http://127.0.0.1:8000/api/post/analytics/?date_from=ex(2023-11-03)&date_to=ex(2023-11-16)",
    "users": "http://127.0.0.1:8000/api/users/",
    "user_activity": "http://127.0.0.1:8000/api/users/user_activity/<int:pk>",

