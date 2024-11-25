from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def create_app():
    # Paths for templates and static files
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'templates')

    # Initialize the Flask app
    app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)

    # Set the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable a Flask-SQLAlchemy feature that's not needed

    # Bind the database object to the app
    db.init_app(app)

    # Define a route
    @app.route('/')
    def home():
        return "Welcome to AgriConnect!"

    # Initialize the database and tables (if needed)
    with app.app_context():
        db.create_all()  # Create tables

    return app

# If running this script directly, create app instance and run the server
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
