from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
import jwt
import os

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

# Secret key for JWT
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')

class User(UserMixin):
    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

# Mock database - Replace with your actual database
users_db = {}

@login_manager.user_loader
def load_user(user_id):
    return users_db.get(user_id)

@auth.route('/')
def index():
    return render_template('index.html')

@auth.route('/landing')
def landing():
    return render_template('landing.html') 

@auth.route('/docs')
def docs():
    return render_template('docs.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = next((user for user in users_db.values() if user.email == email), None)

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.dashboard'))

    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = next((user for user in users_db.values() if user.email == email), None)

        if user:
            flash('Email address already exists', 'error')
            return redirect(url_for('auth.signup'))

        new_user = User(
            id=str(len(users_db) + 1),
            email=email,
            name=name,
            password=generate_password_hash(password, method='sha256')
        )

        users_db[new_user.id] = new_user
        login_user(new_user)
        return redirect(url_for('main.dashboard'))

    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = next((user for user in users_db.values() if user.email == email), None)
        
        if user:
            token = generate_reset_token(user)
            # In a real application, send this token via email
            flash('Password reset instructions have been sent to your email.', 'info')
            return redirect(url_for('auth.login'))
        
        flash('Email not found.', 'error')
    return render_template('reset_password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = verify_reset_token(token)
        if request.method == 'POST':
            user = next((user for user in users_db.values() if user.email == email), None)
            if user:
                user.password = generate_password_hash(request.form.get('password'), method='sha256')
                flash('Your password has been updated.', 'success')
                return redirect(url_for('auth.login'))
    except:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('auth.reset_password_request'))
    
    return render_template('reset_password_confirm.html')

def generate_reset_token(user):
    return jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm='HS256'
    )

def verify_reset_token(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data['user_id']
    except:
        return None 