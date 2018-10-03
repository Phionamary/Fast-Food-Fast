[![Build Status](https://travis-ci.org/Phionamary/Fast-Food-Fast.svg?branch=Database)](https://travis-ci.org/Phionamary/Fast-Food-Fast)
[![Coverage Status](https://coveralls.io/repos/github/Phionamary/Fast-Food-Fast/badge.svg?branch=Database)](https://coveralls.io/github/Phionamary/Fast-Food-Fast?branch=Database)
[![Maintainability](https://api.codeclimate.com/v1/badges/14ceda9d0603ab17f897/maintainability)](https://codeclimate.com/github/Phionamary/Fast-Food-Fast/maintainability)

# Fast Food Fast
Fast-Food-Fast is a food delivery service app for a restaurant.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
You need to install the following: 
* Server side Framework: ​[Flask Python Framework](http://flask.pocoo.org/)
* Testing Framework: [PyTest](https://docs.pytest.org/en/latest/)
* pip 
* virtual env

### Installing 
These are the series of commands you need to get it up and running on your machine 
#### Clone the repo into your local machine

```
git clone https://github.com/Phionamary/Fast-Food-Fast
```
#### Install virtual environment 
``` 
C:\Users\User>virtualenv venv
```
#### Activate virtual environment
``` 
C:\Users\User>venv\Scripts\activate
``` 

```
(venv) C:\Users\User>
 ```

### Move to the directory of the cloned repository folder
  ```
   (venv)cd E:\repos\Fast-Food-Fast
  ```
#### Install modules required for the app 
```
(venv) $ pip install>requirements.txt
```
#### Create database by running the following command
```
psql -c 'CREATE DATABASE fastfoodfast;' -U postgres
```
### Run the server with the command
```
python -m flask run 
```

### Running Tests
* Install nosetests and coverage
  ```
  $ pip install nose coverage
  ```

* Running the tests
  * Setup test database
  ```
  psql -c 'CREATE DATABASE fastfoodfast;' -U postgres
  ```
  * Set the environment variable
  ```
  $ set app_env=testing
  ```
  * Run the tests
  ```
  $ nosetests -v --with-coverage --cover-package=tests
  ```
## Features
* Create user accounts that can signin/signout from the app. 
* Place an order for food.
* Get list of orders.
* Get a specific order.
* Update the status of an order. 
* Get the menu.
* Add food option to the menu.
* View the order history  for a particular user.



## Access at:
### https://phionamary.github.io/Fast-Food-Fast/UI/index.html
### https://fast-foods-fast-app.herokuapp.com/api/v1/orders


 ## API endpoints

END POINT | METHOD | USE
--------- | ---- | -----
/api/v1/auth/login | POST | User sign in
/api/v1/auth/signup | POST | User sign up
/api/v1/| GET | API prefix
/api/v1/orders | GET | Gets a list of all orders
/api/v1/orders/<int:Request_ID> | GET | Get a particular order with a given ID
/api/v1/orders/<int:User_id> | POST | Make a new order
/api/v1/orders/<int:Request_ID> | PUT | Update order status for an order with a given ID

## Authors
* Kigai Phiona Mary
