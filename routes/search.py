"""
Search Routes
Handles order search functionality.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from database.database import db
from config import config
from routes.auth import login_required

search_bp = Blueprint('search', __name__, url_prefix='/search')


@search_bp.route('/', methods=['GET', 'POST'])
@login_required
def search_orders():
    """Search orders by multiple criteria"""
    results = []
    search_type = ''
    search_term = ''
    
    if request.method == 'POST':
        search_type = request.form.get('search_type', '').strip()
        search_term = request.form.get('search_term', '').strip()
        
        if not search_term:
            flash('Please enter a search term.', 'error')
            return redirect(url_for('search.search_orders'))
        
        valid_search_types = ['order_id', 'customer_name', 'product_name', 'tracking_number', 'status']
        
        if search_type not in valid_search_types:
            flash('Invalid search type.', 'error')
            return redirect(url_for('search.search_orders'))
        
        try:
            results = db.search_orders(search_term, search_type)
            
            if not results:
                flash(f'No orders found matching "{search_term}".', 'info')
        
        except Exception as e:
            print(f"Error searching orders: {e}")
            flash('Error performing search.', 'error')
    
    return render_template('search_orders.html', 
                         results=results,
                         search_type=search_type,
                         search_term=search_term,
                         statuses=config.ORDER_STATUSES)