"""
Django CRUD Sundae plugins for the articles demo app.

This file demonstrates how to register plugins in a Django app.
"""
from sundae.plugins import BasePlugin

# Import the example plugins
from .sundae_plugin_widgets import AdvancedWidgetsPlugin
from .sundae_plugin_datatables import DataTablesPlugin


class SundaePlugin(BasePlugin):
    """
    Main plugin for the articles app.

    This plugin serves as an entry point and registers other plugins.
    """
    name = "articles_demo"
    version = "1.0.0"
    description = "Demo plugins for Django CRUD Sundae"
    author = "Django CRUD Sundae Team"

    def register(self, registry):
        """Register all demo plugins"""
        # Register the widgets plugin
        widgets_plugin = AdvancedWidgetsPlugin()
        registry.register('sundae_advanced_widgets', widgets_plugin)

        # Register the datatables plugin
        datatables_plugin = DataTablesPlugin()
        registry.register('sundae_datatables', datatables_plugin)

    def ready(self):
        """Called after all plugins are loaded."""
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Articles demo plugins v{self.version} ready")
