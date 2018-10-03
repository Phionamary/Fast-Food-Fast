"""File to start the flask app"""
from app.app import app


if __name__ == '__main__':
    app.run(debug=True)