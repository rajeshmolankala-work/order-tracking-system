"""
Configuration Module
Manages all application settings, constants, and environment variables.
"""

import os
from datetime import timedelta

# Get the base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Ensure database and export directories exist
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'exports')
DATABASE_FOLDER = os.path.join(BASE_DIR, 'database')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)


class Config:
    """Base configuration class with all settings"""
    
    # Flask Core Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'order-tracking-system-secret-key-2024')
    DEBUG = False
    TESTING = False
    
    # Database Configuration
    DATABASE_PATH = os.path.join(DATABASE_FOLDER, 'orders.db')
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # File Upload Configuration
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Application Constants
    APP_NAME = 'Order Tracking System'
    APP_VERSION = '1.0.0'
    
    # Admin Credentials
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'
    
    # Order Configuration
    ORDER_STATUSES = [
        'Pending',
        'Processing',
        'Packed',
        'Shipped',
        'Out for Delivery',
        'Delivered',
        'Cancelled'
    ]
    
    PAYMENT_STATUSES = [
        'Pending',
        'Completed',
        'Failed',
        'Refunded'
    ]
    
    # Pagination Settings
    ITEMS_PER_PAGE = 10
    
    # Date/Time Formats
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DISPLAY_DATE_FORMAT = '%d %b %Y'
    DISPLAY_DATETIME_FORMAT = '%d %b %Y %H:%M'


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DATABASE_PATH = os.path.join(DATABASE_FOLDER, 'test_orders.db')


# Select configuration based on environment
def get_config():
    """Get configuration based on FLASK_ENV environment variable"""
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig


# Export configuration
config = get_config()