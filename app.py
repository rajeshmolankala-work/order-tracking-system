"""
Main Flask Application
Initializes Flask app, registers blueprints, and configures the application.
"""

from flask import Flask, render_template, redirect, url_for, session
from flask_session import Session
from config import config
from routes import auth_bp, dashboard_bp, orders_bp, search_bp, reports_bp, export_bp
import os

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(config)

# Configure session
Session(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(search_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(export_bp)


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('500.html'), 500


# Root route redirect
@app.route('/', methods=['GET'])
def root():
    """Redirect to dashboard or login"""
    if 'user' in session:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))


# Context processor for global variables
@app.context_processor
def inject_app_info():
    """Make app info available to all templates"""
    return {
        'app_name': config.APP_NAME,
        'app_version': config.APP_VERSION
    }


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('exports', exist_ok=True)
    os.makedirs('database', exist_ok=True)
    os.makedirs(os.path.join('static', 'css'), exist_ok=True)
    os.makedirs(os.path.join('static', 'js'), exist_ok=True)
    os.makedirs(os.path.join('templates'), exist_ok=True)
    
    # Run the application
    print("=" * 60)
    print("Order Tracking System")
    print("=" * 60)
    print("Starting Flask application...")
    print("Access the application at: http://127.0.0.1:5000")
    print("Login with: admin / admin123")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)