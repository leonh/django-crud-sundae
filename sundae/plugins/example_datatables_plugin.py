"""
Example plugin: DataTables integration for Django CRUD Sundae.

This plugin demonstrates how to create a Sundae plugin that:
- Adds DataTables to list views
- Customizes templates
- Adds CSS/JS files
- Modifies list context
"""
from sundae.plugins import BasePlugin


class DataTablesPlugin(BasePlugin):
    """
    Plugin that adds DataTables functionality to list views.
    """

    name = "sundae_datatables"
    version = "1.0.0"
    description = "Adds interactive DataTables to Django CRUD Sundae list views"
    author = "Your Name"

    def register(self, registry):
        """Register plugin hooks."""
        # Add CSS/JS files
        registry.register_hook('get_css_files', self.get_css_files, priority=10)
        registry.register_hook('get_js_files', self.get_js_files, priority=10)

        # Modify list view context
        registry.register_hook('filter_list_context', self.add_datatables_config, priority=20)

        # Add initialization script to templates
        registry.register_hook('template_body_end', self.add_init_script, priority=30)

        # Override list template
        registry.register_hook('get_template_names', self.override_list_template, priority=5)

    def get_css_files(self, **kwargs):
        """Return DataTables CSS files."""
        return [
            'https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css',
            'https://cdn.datatables.net/responsive/2.5.0/css/responsive.bootstrap5.min.css',
            'https://cdn.datatables.net/buttons/2.4.1/css/buttons.bootstrap5.min.css',
        ]

    def get_js_files(self, **kwargs):
        """Return DataTables JavaScript files."""
        return [
            'https://code.jquery.com/jquery-3.7.0.min.js',
            'https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js',
            'https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js',
            'https://cdn.datatables.net/responsive/2.5.0/js/dataTables.responsive.min.js',
            'https://cdn.datatables.net/buttons/2.4.1/js/dataTables.buttons.min.js',
            'https://cdn.datatables.net/buttons/2.4.1/js/buttons.html5.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js',
        ]

    def add_datatables_config(self, context, **kwargs):
        """Add DataTables configuration to context."""
        view = kwargs.get('view')

        if view and hasattr(view, 'template_name_suffix') and view.template_name_suffix == '_list':
            # Add DataTables configuration
            context['datatables_enabled'] = True
            context['datatables_config'] = self.get_datatables_config(view)

        return context

    def get_datatables_config(self, view):
        """Generate DataTables configuration based on view settings."""
        config = self.get_config()

        return {
            'pageLength': config.get('page_length', 25),
            'responsive': config.get('responsive', True),
            'dom': config.get('dom', 'Bfrtip'),
            'buttons': config.get('buttons', ['copy', 'csv', 'excel', 'pdf', 'print']),
            'order': config.get('order', [[0, 'asc']]),
            'language': {
                'search': 'Filter:',
                'lengthMenu': 'Show _MENU_ entries',
                'info': 'Showing _START_ to _END_ of _TOTAL_ entries',
                'paginate': {
                    'first': 'First',
                    'last': 'Last',
                    'next': 'Next',
                    'previous': 'Previous'
                }
            }
        }

    def add_init_script(self, **kwargs):
        """Add DataTables initialization script."""
        context = kwargs.get('context', {})

        if context.get('datatables_enabled'):
            config = context.get('datatables_config', {})

            # Convert Python config to JavaScript
            import json
            config_json = json.dumps(config)

            return f"""
            <script>
            $(document).ready(function() {{
                // Initialize DataTables on admin tables
                $('.table-admin').DataTable({config_json});

                // Custom styling for Tailwind CSS
                $('.dataTables_wrapper').addClass('p-4');
                $('.dataTables_filter input').addClass('form-select ml-2');
                $('.dataTables_length select').addClass('form-select ml-2 mr-2');
            }});
            </script>
            """

        return ""

    def override_list_template(self, **kwargs):
        """Override list template if configured."""
        suffix = kwargs.get('suffix')

        # Only override list templates
        if suffix == '_list':
            config = self.get_config()
            if config.get('override_template', False):
                return ['sundae_datatables/object_list.html']

        return None

    def ready(self):
        """Called after all plugins are loaded."""
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"DataTables plugin v{self.version} ready")


# This allows the plugin to be discovered
SundaePlugin = DataTablesPlugin