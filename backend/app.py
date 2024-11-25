from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def create_app():
    # Paths for templates and static files
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')  # Update if necessary
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')  # Update if necessary

    # Initialize the Flask app
    app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)
    
    # Secret key for sessions
    app.secret_key = 'your_secret_key'  # Change to a strong key for production

    # Set the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable a Flask-SQLAlchemy feature that's not needed

    # Bind the database object to the app
    db.init_app(app)

    # Define a User model
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100), unique=True, nullable=False)
        password = db.Column(db.String(100), nullable=False)
        role = db.Column(db.String(50), nullable=False)  # Role can be 'user', 'admin', or 'supplier'

    # Define a route to render the home page
    @app.route('/')
    def home():
        return render_template('home.html')  # Make sure this matches your HTML file name
    
    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Fetch user from database
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:  # In a real app, use hashed passwords
                session['user_id'] = user.id  # Save user id in session
                session['role'] = user.role    # Save user role in session

                # Redirect based on the role
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                elif user.role == 'supplier':
                    return redirect(url_for('supplier_dashboard'))
                else:
                    return redirect(url_for('user_dashboard'))
            else:
                return "Invalid credentials, please try again.", 401

        return render_template('signin.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']  # Role can be selected at sign up
            
            # Create new user
            new_user = User(username=username, password=password, role=role)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('signin'))

        return render_template('signup.html')

    # User dashboards
    @app.route('/user-dashboard')
    def user_dashboard():
        return render_template('user_dashboard.html')
    
    @app.route('/admin-dashboard')
    def admin_dashboard():
        return render_template('admin_dashboard.html')

    @app.route('/supplier-dashboard')
    def supplier_dashboard():
        return render_template('supplier_dashboard.html')

    # Initialize the database and tables (if needed)
    with app.app_context():
        db.create_all()  # Create tables

    return app

# If running this script directly, create app instance and run the server
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
