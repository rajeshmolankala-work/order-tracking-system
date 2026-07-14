"""
Authentication Routes
Handles login, logout, and session management.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import config
from functools import wraps

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if 'user' in session:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return redirect(url_for('auth.login'))
        
        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session['user'] = username
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username or password.', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Handle user logout"""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login first.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    
    return decorated_function