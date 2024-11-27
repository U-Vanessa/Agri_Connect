from flask import Flask, render_template, redirect, url_for, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def create_app():
    # Paths for templates and static files
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

    # Initialize the Flask app
    app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)
    
    # Secret key for sessions
    app.secret_key = os.urandom(24)  # Generate a strong random key

    # Set the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind the database object to the app
    db.init_app(app)

    # Define a User model
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(100), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
        role = db.Column(db.String(50), nullable=False)  # Role can be 'cust', 'farm', 'supp'

    @app.route('/')
    @app.route('/home')
    def home():
        return render_template('set.html')
    
     
    # Function to create example users
    @app.route('/create-example-users')
    def create_example_users():
        if User.query.first():
            return "Example users already exist!"

        example_users = [
            {'username': 'user1', 'password': 'password1', 'role': 'cust'},
            {'username': 'farmer1', 'password': 'password2', 'role': 'farm'},
            {'username': 'supplier1', 'password': 'password3', 'role': 'supp'}
        ]
        
        for user in example_users:
            hashed_password = generate_password_hash(user['password'])
            new_user = User(username=user['username'], password=hashed_password, role=user['role'])
            db.session.add(new_user)
        
        db.session.commit()
        return "Example users created!"

    # Home page route
    
    
    # Sign-in route
    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Fetch user from database
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):  # Verify hashed password
                session['user_id'] = user.id  # Save user id in session
                session['role'] = user.role   # Save user role in session

                # Redirect based on the role
                if user.role == 'farm':
                    return redirect(url_for('farm_dashboard'))
                elif user.role == 'supp':
                    return redirect(url_for('supp_dashboard'))
                else:
                    return redirect(url_for('cust_dashboard'))
            else:
                # Render error message on sign-in page
                return render_template('signin.html', error="Invalid credentials, please try again.")
            
        return render_template('signin.html')

    # Role-based dashboards
    @app.route('/cust')
    def cust_dashboard():
        if session.get('role') != 'cust':
            abort(403)  # Access forbidden
        return render_template('cust.html')
    
    @app.route('/farm')
    def farm_dashboard():
        if session.get('role') != 'farm':
            abort(403)
        return render_template('farm.html')

    @app.route('/supp')
    def supp_dashboard():
        if session.get('role') != 'supp':
            abort(403)
        return render_template('supp.html')

    # Log out route
    @app.route('/logout')
    def logout():
        session.clear()  # Clear the session
        return redirect(url_for('home'))

    # Error handlers for better debugging
    @app.errorhandler(403)
    def forbidden(error):
        return "403 Forbidden: You do not have permission to access this resource.", 403

    @app.errorhandler(404)
    def page_not_found(error):
        return "404 Not Found: The page you are looking for does not exist.", 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return "500 Internal Server Error: Something went wrong on our end.", 500

    # Initialize the database and tables
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    return app

# If running this script directly, create app instance and run the server
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
