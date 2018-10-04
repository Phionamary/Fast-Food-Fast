"""File to start the flask app"""
from app.app import app
from models import DatabaseConnection


if __name__ == '__main__':
    DatabaseConnection().create_menu_table()
    DatabaseConnection().create_orders_table()
    DatabaseConnection().create_users_table()
    app.run(debug=True)
