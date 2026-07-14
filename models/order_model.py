"""
Order Model
Handles order data validation, serialization, and business logic.
"""

import re
from datetime import datetime
from config import config


class Order:
    """Order data model with comprehensive validation"""
    
    def __init__(self, order_data):
        """Initialize order with data"""
        self.order_id = order_data.get('order_id', '').strip()
        self.customer_name = order_data.get('customer_name', '').strip()
        self.product_name = order_data.get('product_name', '').strip()
        self.quantity = order_data.get('quantity', 0)
        self.price = order_data.get('price', 0)
        self.order_date = order_data.get('order_date', '').strip()
        self.delivery_date = order_data.get('delivery_date', '').strip()
        self.status = order_data.get('status', 'Pending').strip()
        self.payment_status = order_data.get('payment_status', 'Pending').strip()
        self.tracking_number = order_data.get('tracking_number', '').strip()
        self.shipping_address = order_data.get('shipping_address', '').strip()
        self.contact_number = order_data.get('contact_number', '').strip()
    
    def validate(self):
        """Validate all order fields"""
        errors = []
        
        # Order ID validation
        if not self.order_id:
            errors.append('Order ID is required.')
        elif not re.match(r'^[A-Z0-9\-]{3,20}$', self.order_id):
            errors.append('Order ID must be 3-20 characters (letters, numbers, hyphens only).')
        
        # Customer name validation
        if not self.customer_name:
            errors.append('Customer name is required.')
        elif len(self.customer_name) < 2 or len(self.customer_name) > 100:
            errors.append('Customer name must be between 2 and 100 characters.')
        elif not re.match(r'^[a-zA-Z\s\-\.]+$', self.customer_name):
            errors.append('Customer name can only contain letters, spaces, hyphens, and periods.')
        
        # Product name validation
        if not self.product_name:
            errors.append('Product name is required.')
        elif len(self.product_name) < 2 or len(self.product_name) > 100:
            errors.append('Product name must be between 2 and 100 characters.')
        
        # Quantity validation
        try:
            qty = int(self.quantity)
            if qty <= 0:
                errors.append('Quantity must be greater than 0.')
        except (ValueError, TypeError):
            errors.append('Quantity must be a valid number.')
        
        # Price validation
        try:
            price = float(self.price)
            if price < 0:
                errors.append('Price cannot be negative.')
        except (ValueError, TypeError):
            errors.append('Price must be a valid number.')
        
        # Order date validation
        if not self.order_date:
            errors.append('Order date is required.')
        else:
            if not self._is_valid_date(self.order_date):
                errors.append('Order date must be in YYYY-MM-DD format.')
        
        # Delivery date validation
        if self.delivery_date and not self._is_valid_date(self.delivery_date):
            errors.append('Delivery date must be in YYYY-MM-DD format.')
        
        # Status validation
        if self.status not in config.ORDER_STATUSES:
            errors.append(f'Invalid status.')
        
        # Payment status validation
        if self.payment_status not in config.PAYMENT_STATUSES:
            errors.append(f'Invalid payment status.')
        
        # Tracking number validation
        if self.tracking_number and len(self.tracking_number) > 50:
            errors.append('Tracking number must be 50 characters or less.')
        
        # Shipping address validation
        if not self.shipping_address:
            errors.append('Shipping address is required.')
        elif len(self.shipping_address) < 5 or len(self.shipping_address) > 250:
            errors.append('Shipping address must be between 5 and 250 characters.')
        
        # Contact number validation
        if not self.contact_number:
            errors.append('Contact number is required.')
        elif not re.match(r'^[0-9\-\+\(\)\s]{10,20}$', self.contact_number):
            errors.append('Contact number must be valid.')
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _is_valid_date(date_str):
        """Validate date format YYYY-MM-DD"""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'order_id': self.order_id,
            'customer_name': self.customer_name,
            'product_name': self.product_name,
            'quantity': int(self.quantity),
            'price': float(self.price),
            'order_date': self.order_date,
            'delivery_date': self.delivery_date,
            'status': self.status,
            'payment_status': self.payment_status,
            'tracking_number': self.tracking_number,
            'shipping_address': self.shipping_address,
            'contact_number': self.contact_number
        }
    
    def calculate_total(self):
        """Calculate total price"""
        try:
            return int(self.quantity) * float(self.price)
        except (ValueError, TypeError):
            return 0