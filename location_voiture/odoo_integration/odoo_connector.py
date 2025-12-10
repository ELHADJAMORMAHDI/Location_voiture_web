"""
Odoo Integration Module

This module provides utilities to connect and synchronize data with Odoo ERP.
Supports both XML-RPC and REST API methods.

Usage:
    from odoo_integration.odoo_connector import OdooConnector
    connector = OdooConnector()
    cars = connector.fetch_cars()
"""

from .odoo_connector import OdooConnector
from .sync_manager import SyncManager

__all__ = ['OdooConnector', 'SyncManager']
