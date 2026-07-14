"""
Reports Routes
Generates various reports for orders and revenue analysis.
"""

from flask import Blueprint, render_template, request, flash
from database.database import db
from config import config
from routes.auth import login_required
from datetime import datetime

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


@reports_bp.route('/', methods=['GET', 'POST'])
@login_required
def generate_reports():
    """Generate reports based on date range and filters"""
    report_data = {
        'daily_orders': [],
        'weekly_orders': [],
        'monthly_orders': [],
        'pending_orders': [],
        'delivered_orders': [],
        'cancelled_orders': [],
        'revenue_total': 0
    }
    
    if request.method == 'POST':
        try:
            report_type = request.form.get('report_type', 'daily').strip()
            start_date_str = request.form.get('start_date', '').strip()
            end_date_str = request.form.get('end_date', '').strip()
            
            if not start_date_str or not end_date_str:
                flash('Please select both start and end dates.', 'error')
                return render_template('reports.html', report_data=report_data)
            
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
                return render_template('reports.html', report_data=report_data)
            
            if start_date > end_date:
                flash('Start date cannot be after end date.', 'error')
                return render_template('reports.html', report_data=report_data)
            
            all_orders = db.get_orders_by_date_range(start_date_str, end_date_str)
            pending_orders = db.get_orders_by_status_and_date_range('Pending', start_date_str, end_date_str)
            delivered_orders = db.get_orders_by_status_and_date_range('Delivered', start_date_str, end_date_str)
            cancelled_orders = db.get_orders_by_status_and_date_range('Cancelled', start_date_str, end_date_str)
            
            revenue_total = sum(order['price'] * order['quantity'] for order in delivered_orders)
            
            if report_type == 'daily':
                report_data['daily_orders'] = all_orders
            elif report_type == 'weekly':
                report_data['weekly_orders'] = all_orders
            elif report_type == 'monthly':
                report_data['monthly_orders'] = all_orders
            
            report_data['pending_orders'] = pending_orders
            report_data['delivered_orders'] = delivered_orders
            report_data['cancelled_orders'] = cancelled_orders
            report_data['revenue_total'] = f"{revenue_total:.2f}"
            report_data['total_orders'] = len(all_orders)
            report_data['report_type'] = report_type
            report_data['start_date'] = start_date_str
            report_data['end_date'] = end_date_str
            report_data['date_range'] = f"{start_date_str} to {end_date_str}"
        
        except Exception as e:
            print(f"Error generating report: {e}")
            flash('Error generating report.', 'error')
    
    return render_template('reports.html', report_data=report_data)


@reports_bp.route('/pending', methods=['GET'])
@login_required
def pending_orders_report():
    """Get all pending orders"""
    try:
        pending_orders = db.get_orders_by_status('Pending')
        return render_template('reports.html', 
                             report_data={'pending_orders': pending_orders},
                             title='Pending Orders Report')
    except Exception as e:
        print(f"Error generating pending orders report: {e}")
        flash('Error generating report.', 'error')
        return render_template('reports.html')


@reports_bp.route('/delivered', methods=['GET'])
@login_required
def delivered_orders_report():
    """Get all delivered orders"""
    try:
        delivered_orders = db.get_orders_by_status('Delivered')
        total_revenue = sum(order['price'] * order['quantity'] for order in delivered_orders)
        
        return render_template('reports.html', 
                             report_data={'delivered_orders': delivered_orders, 'revenue_total': total_revenue},
                             title='Delivered Orders Report')
    except Exception as e:
        print(f"Error generating delivered orders report: {e}")
        flash('Error generating report.', 'error')
        return render_template('reports.html')