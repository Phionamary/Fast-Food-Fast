"""File to start the flask app"""
from app.app import app
from app.models import DatabaseConnection


if __name__ == '__main__':
    app.run(debug=True)
