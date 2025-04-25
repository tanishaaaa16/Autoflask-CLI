def setup_authentication(project_name):
    """Setup authentication files and templates for the project"""
    print("Setting up Flask Authentication with SQLAlchemy...")
    try:
        # Create database models
        with open('models.py', 'w') as f:
            f.write("""from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
""")

        # Create authentication routes
        with open('auth.py', 'w') as f:
            f.write("""from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models import User, db
from bcrypt import hashpw, gensalt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        new_user = User(username=username, password=hashed_password.decode('utf-8'))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and hashpw(password.encode('utf-8'), user.password.encode('utf-8')) == user.password.encode('utf-8'):
            login_user(user)
            return redirect(url_for('protected'))  # Redirect to your home page

        flash('Invalid username or password')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
""")

        # Create app.py with authentication
        with open('app.py', 'w') as f:
            f.write(f"""from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from auth import auth_bp, User
from models import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{project_name}.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications

db.init_app(app)  # Initialize SQLAlchemy

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Where to redirect if not logged in

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True,host='0.0.0.0')
""")

        # Create auth templates
        create_auth_templates()
        
        print("Flask Authentication setup complete.")
        return True

    except OSError as e:
        print(f"Failed to create authentication files: {e}")
        return False

def create_auth_templates():
    """Create templates for authentication"""
    try:
        # Create login template
        with open('templates/login.html', 'w') as f:
            f.write("""{% extends "base.html" %}
{% block content %}
<h2>Login</h2>
<form method="POST">
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Login</button>
</form>
{% endblock %}
{% block css %}

{% endblock %}
{% block js %}

{% endblock %}
""")

        # Create register template
        with open('templates/register.html', 'w') as f:
            f.write("""{% extends "base.html" %}
{% block content %}
<h2>Register</h2>
<form method="POST">
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Register</button>
</form>
{% endblock %}
{% block css %}

{% endblock %}
{% block js %}

{% endblock %}
""")

        # Create protected template
        with open('templates/protected.html', 'w') as f:
            f.write("""{% extends "base.html" %}
{% block content %}
<h2>Protected Page</h2>
<p>You are logged in!</p>
<a href="{{ url_for('auth.logout') }}">Logout</a>
{% endblock %}
{% block css %}

{% endblock %}
{% block js %}

{% endblock %}
""")
        
        return True
    except OSError as e:
        print(f"Failed to create authentication templates: {e}")
        return False
    
if __name__ == "__main__":
    # Example usage
    project_name = "my_flask_app"
    setup_authentication(project_name)
    # setup_authentication(project_name)