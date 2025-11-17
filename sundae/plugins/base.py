from collections import defaultdict

# sundae/plugins/base.py
from typing import Optional
from abc import ABC

class BasePlugin(ABC):
    """Base class for all Sundae plugins"""

    name: Optional[str] = None
    version: str = "1.0.0"
    description: str = ""
    author: str = ""

    def register(self, registry: 'PluginRegistry'):
        """
        Called during plugin registration.
        Override this to register hooks, widgets, etc.

        Args:
            registry: The PluginRegistry instance
        """
        pass

    def ready(self):
        """
        Called after all plugins are registered.
        Override this for initialization that depends on other plugins.
        """
        pass

    def get_config(self):
        """Get plugin configuration from settings"""
        from django.conf import settings
        plugin_config = getattr(settings, 'SUNDAE_PLUGINS', {})
        return plugin_config.get('config', {}).get(self.name, {})


class PluginRegistry:
    """Central registry for all plugins"""
    _hooks = defaultdict(list)
    _plugins = {}
    _widget_mappings = {}
    _view_mixins = []

    @classmethod
    def register_hook(cls, hook_name, callback, priority=50):
        """Register a callback for a specific hook"""
        cls._hooks[hook_name].append((priority, callback))
        cls._hooks[hook_name].sort(key=lambda x: x[0])

    @classmethod
    def register_widget(cls, field_type, widget_class):
        """Register custom widget for field type"""
        cls._widget_mappings[field_type] = widget_class

    @classmethod
    def register_view_mixin(cls, mixin_class):
        """Register a mixin to be added to CRUDSundaeView"""
        cls._view_mixins.append(mixin_class)

class SundaePlugin:
    """Base class for all plugins"""
    name = None
    version = None

    def ready(self):
        """Called when plugin is loaded"""
        pass