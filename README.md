
[![Build Status](https://travis-ci.org/Phionamary/Fast-Food-Fast.svg?branch=Feature)](https://travis-ci.org/Phionamary/Fast-Food-Fast)
[![Coverage Status](https://coveralls.io/repos/github/Phionamary/Fast-Food-Fast/badge.svg?branch=Feature)](https://coveralls.io/github/Phionamary/Fast-Food-Fast?branch=Feature)
[![Maintainability](https://api.codeclimate.com/v1/badges/14ceda9d0603ab17f897/maintainability)](https://codeclimate.com/github/Phionamary/Fast-Food-Fast/maintainability)


# Fast-Food-Fast

Fast-Food-Fast is a food delivery service app for a restaurant.

# Main requirements include:
1. git
2. python
3. pip
4. virtualenv


# Getting Started
1. Clone the project
git clone ```https://github.com/Phionamary/Fast-Food-Fast.git```

2. Create a virtual environment using ```virtualenv``` and activate it.
```virtualenv venv``` ```venv\Scripts\Activate```

3. Install packages using ```pip install -r requirements.txt```

4. Run the app by running ```run.py```

```python run.py```

# Project Link
Interface The link to the pages hosted on gh-pages is: https://phionamary.github.io/Fast-Food-Fast/UI/index.html

The link to git hub feature branch with the code is: https://github.com/Phionamary/Fast-Food-Fast/tree/Feature 

## API endpoints

The link to the git hub branch with the code is: https://github.com/Phionamary/Fast-Food-Fast/tree/Feature/rest_api

The link to the hosted apis on heroku: https://fast-foods-fast-app.herokuapp.com/api/v1/orders

Features interface

* Users can create accounts and sign in.
* Users can order for food.
* Admins can do the following:
    * See a list of orders.
    * Accept and decline orders.
    * Mark orders as completed.
* Users see a history of ordered food.


## API endpoints

End Point | Verb | Use
--------- | ---- | -----
/api/v1/| GET | API prefix
/api/v1/orders | GET | Gets a list of all orders
/api/v1/orders/<int:Request_ID> | GET | Get a particular order with a given ID
/api/v1/orders | POST | Make a new order
/api/v1/orders/<int:Request_ID> | DELETE | Delete an order resource of a given ID
/api/v1/orders/<int:Request_ID> | PUT | Update order status for an order with a given ID


# Built With

## Interface

* HTML5
* CSS


## API endpoints

* Python 3
* Flask
* Flask restful


# Prerequisites
* HTML 5
* Internet


# Authors
Kigai Phiona Mary

# Licensing
The app is opensource hence free to all users

* Web browser with support for HTML5
* Internet connection
