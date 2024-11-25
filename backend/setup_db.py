import sys
import os

# Add the parent directory (AgriConnect) to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app, db  # Import from the backend module

app = create_app()

with app.app_context():
    db.create_all()
    print("Database initialized successfully!")
