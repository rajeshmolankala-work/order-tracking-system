"""
Database Module
Handles SQLite connection, schema creation, and all CRUD operations.
"""

import sqlite3
import os
from datetime import datetime
from config import config


class Database:
    """Database connection and operations manager"""
    
    def __init__(self):
        """Initialize database connection"""
        self.db_path = config.DATABASE_PATH
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            self.create_schema()
    
    def get_connection(self):
        """Get SQLite database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_schema(self):
        """Create database schema with all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Orders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT UNIQUE NOT NULL,
                    customer_name TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    order_date TEXT NOT NULL,
                    delivery_date TEXT,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    payment_status TEXT NOT NULL DEFAULT 'Pending',
                    tracking_number TEXT,
                    shipping_address TEXT NOT NULL,
                    contact_number TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Order Status History table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_status_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT NOT NULL,
                    old_status TEXT,
                    new_status TEXT NOT NULL,
                    changed_at TEXT NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id)
                )
            ''')
            
            # Create indexes for better query performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_order_id ON orders(order_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON orders(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_customer_name ON orders(customer_name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date)')
            
            conn.commit()
            print(f"✓ Database initialized successfully")
        except sqlite3.Error as e:
            print(f"Error creating database schema: {e}")
            raise
        finally:
            conn.close()
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        """Execute a database query"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                result = cursor.fetchone()
                conn.close()
                return dict(result) if result else None
            elif fetch_all:
                result = cursor.fetchall()
                conn.close()
                return [dict(row) for row in result]
            else:
                if commit:
                    conn.commit()
                lastrowid = cursor.lastrowid
                conn.close()
                return lastrowid
        
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
    
    def insert_order(self, order_data):
        """Insert a new order"""
        query = '''
            INSERT INTO orders (
                order_id, customer_name, product_name, quantity, price,
                order_date, delivery_date, status, payment_status,
                tracking_number, shipping_address, contact_number,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        now = datetime.now().strftime(config.DATETIME_FORMAT)
        
        params = (
            order_data['order_id'],
            order_data['customer_name'],
            order_data['product_name'],
            int(order_data['quantity']),
            float(order_data['price']),
            order_data['order_date'],
            order_data.get('delivery_date', '') or None,
            order_data.get('status', 'Pending'),
            order_data.get('payment_status', 'Pending'),
            order_data.get('tracking_number', '') or None,
            order_data['shipping_address'],
            order_data['contact_number'],
            now,
            now
        )
        
        return self.execute_query(query, params, commit=True)
    
    def get_all_orders(self):
        """Fetch all orders from database"""
        query = 'SELECT * FROM orders ORDER BY created_at DESC'
        return self.execute_query(query, fetch_all=True)
    
    def get_order_by_id(self, order_id):
        """Fetch order by order_id"""
        query = 'SELECT * FROM orders WHERE order_id = ?'
        return self.execute_query(query, (order_id,), fetch_one=True)
    
    def get_order_by_pk(self, pk):
        """Fetch order by primary key (id)"""
        query = 'SELECT * FROM orders WHERE id = ?'
        return self.execute_query(query, (pk,), fetch_one=True)
    
    def update_order(self, order_id, order_data):
        """Update an existing order"""
        now = datetime.now().strftime(config.DATETIME_FORMAT)
        
        query = '''
            UPDATE orders SET
                customer_name = ?,
                product_name = ?,
                quantity = ?,
                price = ?,
                delivery_date = ?,
                status = ?,
                payment_status = ?,
                tracking_number = ?,
                shipping_address = ?,
                contact_number = ?,
                updated_at = ?
            WHERE order_id = ?
        '''
        
        params = (
            order_data['customer_name'],
            order_data['product_name'],
            int(order_data['quantity']),
            float(order_data['price']),
            order_data.get('delivery_date', '') or None,
            order_data.get('status', 'Pending'),
            order_data.get('payment_status', 'Pending'),
            order_data.get('tracking_number', '') or None,
            order_data['shipping_address'],
            order_data['contact_number'],
            now,
            order_id
        )
        
        return self.execute_query(query, params, commit=True)
    
    def delete_order(self, order_id):
        """Delete an order"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM order_status_history WHERE order_id = ?', (order_id,))
            cursor.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))
            
            conn.commit()
            rows_deleted = cursor.rowcount
            conn.close()
            return rows_deleted
        
        except sqlite3.Error as e:
            print(f"Error deleting order: {e}")
            raise
    
    def get_orders_by_status(self, status):
        """Get orders filtered by status"""
        query = 'SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC'
        return self.execute_query(query, (status,), fetch_all=True)
    
    def record_status_change(self, order_id, old_status, new_status):
        """Record a status change in the history table"""
        query = '''
            INSERT INTO order_status_history (order_id, old_status, new_status, changed_at)
            VALUES (?, ?, ?, ?)
        '''
        
        now = datetime.now().strftime(config.DATETIME_FORMAT)
        params = (order_id, old_status, new_status, now)
        
        return self.execute_query(query, params, commit=True)
    
    def search_orders(self, search_term, search_type):
        """Search orders by various criteria"""
        search_types = {
            'order_id': 'order_id LIKE ?',
            'customer_name': 'customer_name LIKE ?',
            'product_name': 'product_name LIKE ?',
            'tracking_number': 'tracking_number LIKE ?',
            'status': 'status LIKE ?'
        }
        
        if search_type not in search_types:
            return []
        
        query = f'SELECT * FROM orders WHERE {search_types[search_type]} ORDER BY created_at DESC'
        search_param = f'%{search_term}%'
        
        return self.execute_query(query, (search_param,), fetch_all=True)
    
    def check_order_id_exists(self, order_id):
        """Check if an order ID already exists"""
        query = 'SELECT COUNT(*) as count FROM orders WHERE order_id = ?'
        result = self.execute_query(query, (order_id,), fetch_one=True)
        return result['count'] > 0 if result else False
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        stats = {}
        
        result = self.execute_query('SELECT COUNT(*) as count FROM orders', fetch_one=True)
        stats['total_orders'] = result['count'] if result else 0
        
        stats['pending_count'] = len(self.get_orders_by_status('Pending'))
        stats['processing_count'] = len(self.get_orders_by_status('Processing'))
        stats['packed_count'] = len(self.get_orders_by_status('Packed'))
        stats['shipped_count'] = len(self.get_orders_by_status('Shipped'))
        stats['out_for_delivery_count'] = len(self.get_orders_by_status('Out for Delivery'))
        stats['delivered_count'] = len(self.get_orders_by_status('Delivered'))
        stats['cancelled_count'] = len(self.get_orders_by_status('Cancelled'))
        
        result = self.execute_query(
            'SELECT SUM(price * quantity) as total FROM orders WHERE status = "Delivered"',
            fetch_one=True
        )
        stats['total_revenue'] = result['total'] if result and result['total'] else 0
        
        stats['recent_orders'] = self.execute_query(
            'SELECT * FROM orders ORDER BY created_at DESC LIMIT 5',
            fetch_all=True
        )
        
        return stats
    
    def get_orders_by_date_range(self, start_date, end_date):
        """Get orders within a date range"""
        query = '''
            SELECT * FROM orders 
            WHERE DATE(order_date) BETWEEN ? AND ?
            ORDER BY order_date DESC
        '''
        return self.execute_query(query, (start_date, end_date), fetch_all=True)
    
    def get_orders_by_status_and_date_range(self, status, start_date, end_date):
        """Get orders filtered by status and date range"""
        query = '''
            SELECT * FROM orders 
            WHERE status = ? AND DATE(order_date) BETWEEN ? AND ?
            ORDER BY order_date DESC
        '''
        return self.execute_query(query, (status, start_date, end_date), fetch_all=True)
    
    def get_status_history(self, order_id):
        """Get status change history for an order"""
        query = '''
            SELECT * FROM order_status_history 
            WHERE order_id = ?
            ORDER BY changed_at DESC
        '''
        return self.execute_query(query, (order_id,), fetch_all=True)
    
    def get_paginated_orders(self, page, per_page):
        """Get paginated orders"""
        offset = (page - 1) * per_page
        
        count_result = self.execute_query('SELECT COUNT(*) as count FROM orders', fetch_one=True)
        total = count_result['count'] if count_result else 0
        
        query = 'SELECT * FROM orders ORDER BY created_at DESC LIMIT ? OFFSET ?'
        orders = self.execute_query(query, (per_page, offset), fetch_all=True)
        
        return orders, total
    
    def get_revenue_by_date_range(self, start_date, end_date):
        """Get total revenue for delivered orders in a date range"""
        query = '''
            SELECT SUM(price * quantity) as total FROM orders
            WHERE status = 'Delivered' AND DATE(order_date) BETWEEN ? AND ?
        '''
        result = self.execute_query(query, (start_date, end_date), fetch_one=True)
        return result['total'] if result and result['total'] else 0


# Initialize global database instance
db = Database()