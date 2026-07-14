"""
Dashboard Routes
Displays dashboard with order statistics and recent orders.
"""

from flask import Blueprint, render_template
from database.database import db
from routes.auth import login_required
from config import config

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')


@dashboard_bp.route('/', methods=['GET'])
@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def index():
    """Display dashboard with statistics"""
    try:
        stats = db.get_dashboard_stats()
        stats['total_revenue'] = f"{stats['total_revenue']:.2f}"
        
        return render_template('dashboard.html', stats=stats, app_name=config.APP_NAME)
    
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        return render_template('dashboard.html', error="Error loading dashboard statistics.")