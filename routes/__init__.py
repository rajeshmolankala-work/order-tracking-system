"""
Routes package initialization
"""

from .auth import auth_bp
from .dashboard import dashboard_bp
from .orders import orders_bp
from .search import search_bp
from .reports import reports_bp
from .export import export_bp

__all__ = ['auth_bp', 'dashboard_bp', 'orders_bp', 'search_bp', 'reports_bp', 'export_bp']