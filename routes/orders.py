"""
Orders Routes
Handles CRUD operations for orders.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database.database import db
from models.order_model import Order
from config import config
from routes.auth import login_required

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/', methods=['GET'])
@login_required
def view_orders():
    """Display all orders with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = config.ITEMS_PER_PAGE
        
        orders, total = db.get_paginated_orders(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        
        return render_template('view_orders.html', 
                             orders=orders, 
                             page=page, 
                             total_pages=total_pages,
                             total_orders=total)
    
    except Exception as e:
        print(f"Error loading orders: {e}")
        flash('Error loading orders.', 'error')
        return redirect(url_for('dashboard.index'))


@orders_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_order():
    """Add a new order"""
    if request.method == 'POST':
        try:
            order_data = {
                'order_id': request.form.get('order_id', '').strip().upper(),
                'customer_name': request.form.get('customer_name', '').strip(),
                'product_name': request.form.get('product_name', '').strip(),
                'quantity': request.form.get('quantity', '0'),
                'price': request.form.get('price', '0'),
                'order_date': request.form.get('order_date', '').strip(),
                'delivery_date': request.form.get('delivery_date', '').strip(),
                'status': request.form.get('status', 'Pending'),
                'payment_status': request.form.get('payment_status', 'Pending'),
                'tracking_number': request.form.get('tracking_number', '').strip(),
                'shipping_address': request.form.get('shipping_address', '').strip(),
                'contact_number': request.form.get('contact_number', '').strip()
            }
            
            order = Order(order_data)
            is_valid, errors = order.validate()
            
            if not is_valid:
                for error in errors:
                    flash(error, 'error')
                return redirect(url_for('orders.add_order'))
            
            if db.check_order_id_exists(order_data['order_id']):
                flash(f'Order ID "{order_data["order_id"]}" already exists.', 'error')
                return redirect(url_for('orders.add_order'))
            
            db.insert_order(order_data)
            db.record_status_change(order_data['order_id'], None, order_data['status'])
            
            flash(f'Order {order_data["order_id"]} added successfully!', 'success')
            return redirect(url_for('orders.view_orders'))
        
        except Exception as e:
            print(f"Error adding order: {e}")
            flash('Error adding order. Please try again.', 'error')
            return redirect(url_for('orders.add_order'))
    
    return render_template('add_order.html', 
                         statuses=config.ORDER_STATUSES,
                         payment_statuses=config.PAYMENT_STATUSES)


@orders_bp.route('/<order_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    """Edit an existing order"""
    order = db.get_order_by_id(order_id)
    
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('orders.view_orders'))
    
    if request.method == 'POST':
        try:
            order_data = {
                'customer_name': request.form.get('customer_name', '').strip(),
                'product_name': request.form.get('product_name', '').strip(),
                'quantity': request.form.get('quantity', '0'),
                'price': request.form.get('price', '0'),
                'delivery_date': request.form.get('delivery_date', '').strip(),
                'status': request.form.get('status', 'Pending'),
                'payment_status': request.form.get('payment_status', 'Pending'),
                'tracking_number': request.form.get('tracking_number', '').strip(),
                'shipping_address': request.form.get('shipping_address', '').strip(),
                'contact_number': request.form.get('contact_number', '').strip()
            }
            
            order_obj = Order({'order_id': order_id, **order_data})
            is_valid, errors = order_obj.validate()
            
            if not is_valid:
                for error in errors:
                    flash(error, 'error')
                return redirect(url_for('orders.edit_order', order_id=order_id))
            
            old_status = order['status']
            new_status = order_data['status']
            
            db.update_order(order_id, order_data)
            
            if old_status != new_status:
                db.record_status_change(order_id, old_status, new_status)
            
            flash(f'Order {order_id} updated successfully!', 'success')
            return redirect(url_for('orders.view_order_details', order_id=order_id))
        
        except Exception as e:
            print(f"Error updating order: {e}")
            flash('Error updating order. Please try again.', 'error')
            return redirect(url_for('orders.edit_order', order_id=order_id))
    
    return render_template('edit_order.html', 
                         order=order,
                         statuses=config.ORDER_STATUSES,
                         payment_statuses=config.PAYMENT_STATUSES)


@orders_bp.route('/<order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id):
    """Delete an order"""
    order = db.get_order_by_id(order_id)
    
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('orders.view_orders'))
    
    try:
        db.delete_order(order_id)
        flash(f'Order {order_id} deleted successfully!', 'success')
    except Exception as e:
        print(f"Error deleting order: {e}")
        flash('Error deleting order. Please try again.', 'error')
    
    return redirect(url_for('orders.view_orders'))


@orders_bp.route('/<order_id>', methods=['GET'])
@login_required
def view_order_details(order_id):
    """Display detailed view of a single order"""
    order = db.get_order_by_id(order_id)
    
    if not order:
        flash('Order not found.', 'error')
        return redirect(url_for('orders.view_orders'))
    
    try:
        status_history = db.get_status_history(order_id)
        total = order['price'] * order['quantity']
        
        return render_template('order_details.html', 
                             order=order, 
                             total=total,
                             status_history=status_history)
    
    except Exception as e:
        print(f"Error loading order details: {e}")
        flash('Error loading order details.', 'error')
        return redirect(url_for('orders.view_orders'))


@orders_bp.route('/<order_id>/update-status', methods=['POST'])
@login_required
def update_status(order_id):
    """Update order status via AJAX"""
    order = db.get_order_by_id(order_id)
    
    if not order:
        return jsonify({'success': False, 'message': 'Order not found'}), 404
    
    try:
        new_status = request.form.get('status', '').strip()
        
        if new_status not in config.ORDER_STATUSES:
            return jsonify({'success': False, 'message': 'Invalid status'}), 400
        
        old_status = order['status']
        
        order_data = dict(order)
        order_data['status'] = new_status
        db.update_order(order_id, order_data)
        
        db.record_status_change(order_id, old_status, new_status)
        
        return jsonify({
            'success': True, 
            'message': f'Status updated to {new_status}',
            'new_status': new_status
        })
    
    except Exception as e:
        print(f"Error updating status: {e}")
        return jsonify({'success': False, 'message': 'Error updating status'}), 500