"""
Example plugin: Advanced Widgets for Django CRUD Sundae.

This plugin demonstrates how to:
- Register custom widgets for field types
- Add date pickers, select2, rich text editors
- Include required CSS/JS files
- Customize form rendering
"""
from sundae.plugins import BasePlugin


class AdvancedWidgetsPlugin(BasePlugin):
    """
    Plugin that adds advanced form widgets to Django CRUD Sundae.
    """

    name = "sundae_advanced_widgets"
    version = "1.0.0"
    description = "Provides advanced form widgets like date pickers, select2, and rich text editors"
    author = "Your Name"

    def register(self, registry):
        """Register plugin components."""
        # Register widget mappings
        registry.register_hook('filter_form_widgets', self.customize_widgets, priority=10)

        # Add CSS/JS files
        registry.register_hook('get_css_files', self.get_css_files, priority=20)
        registry.register_hook('get_js_files', self.get_js_files, priority=20)

        # Add initialization scripts
        registry.register_hook('template_body_end', self.add_widget_init, priority=40)

        # Customize form field rendering
        registry.register_hook('filter_form_class', self.customize_form_class, priority=15)

    def get_css_files(self, **kwargs):
        """Return CSS files for widgets."""
        config = self.get_config()
        css_files = []

        if config.get('use_flatpickr', True):
            css_files.append('https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css')

        if config.get('use_select2', True):
            css_files.append('https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css')

        if config.get('use_quill', True):
            css_files.append('https://cdn.quilljs.com/1.3.6/quill.snow.css')

        return css_files

    def get_js_files(self, **kwargs):
        """Return JavaScript files for widgets."""
        config = self.get_config()
        js_files = []

        if config.get('use_flatpickr', True):
            js_files.append('https://cdn.jsdelivr.net/npm/flatpickr')

        if config.get('use_select2', True):
            js_files.extend([
                'https://code.jquery.com/jquery-3.7.0.min.js',
                'https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js',
            ])

        if config.get('use_quill', True):
            js_files.append('https://cdn.quilljs.com/1.3.6/quill.js')

        return js_files

    def customize_widgets(self, widgets, **kwargs):
        """Customize form widgets based on field types."""
        view = kwargs.get('view')
        config = self.get_config()

        if not view or not view.model:
            return widgets

        # Import Django form widgets
        from django import forms

        for field in view.model._meta.fields:
            field_name = field.name
            field_type = field.__class__.__name__

            # Skip if widget already customized
            if field_name in widgets:
                continue

            # Date/DateTime fields - use Flatpickr
            if config.get('use_flatpickr', True):
                if field_type == 'DateField':
                    widgets[field_name] = forms.DateInput(attrs={
                        'class': 'form-control flatpickr-date',
                        'data-date-format': 'Y-m-d',
                    })
                elif field_type == 'DateTimeField':
                    widgets[field_name] = forms.DateTimeInput(attrs={
                        'class': 'form-control flatpickr-datetime',
                        'data-enable-time': 'true',
                        'data-date-format': 'Y-m-d H:i',
                    })
                elif field_type == 'TimeField':
                    widgets[field_name] = forms.TimeInput(attrs={
                        'class': 'form-control flatpickr-time',
                        'data-no-calendar': 'true',
                        'data-enable-time': 'true',
                        'data-date-format': 'H:i',
                    })

            # ForeignKey/ManyToMany fields - use Select2
            if config.get('use_select2', True):
                if field_type in ['ForeignKey', 'OneToOneField']:
                    widgets[field_name] = forms.Select(attrs={
                        'class': 'form-control select2-single',
                        'data-placeholder': f'Select {field.verbose_name}',
                    })
                elif field_type == 'ManyToManyField':
                    widgets[field_name] = forms.SelectMultiple(attrs={
                        'class': 'form-control select2-multiple',
                        'data-placeholder': f'Select {field.verbose_name}',
                        'multiple': 'multiple',
                    })

            # TextField - use Quill rich text editor
            if config.get('use_quill', True):
                if field_type == 'TextField':
                    # Check if field should use rich text based on name
                    rich_text_fields = config.get('rich_text_fields', [
                        'content', 'body', 'description', 'text', 'html'
                    ])

                    if any(rtf in field_name.lower() for rtf in rich_text_fields):
                        widgets[field_name] = forms.Textarea(attrs={
                            'class': 'form-control quill-editor',
                            'rows': 10,
                        })

            # Choice fields - enhance with better styling
            if hasattr(field, 'choices') and field.choices:
                if len(field.choices) <= 5:
                    # Use radio buttons for small choice sets
                    widgets[field_name] = forms.RadioSelect(attrs={
                        'class': 'form-radio-group',
                    })
                else:
                    # Use enhanced select for larger choice sets
                    widgets[field_name] = forms.Select(attrs={
                        'class': 'form-control enhanced-select',
                    })

        return widgets

    def add_widget_init(self, **kwargs):
        """Add widget initialization JavaScript."""
        context = kwargs.get('context', {})
        view = context.get('view')

        # Only add scripts on form pages
        if not view or not hasattr(view, 'template_name_suffix'):
            return ""

        if view.template_name_suffix not in ['_form', '_create', '_update']:
            return ""

        config = self.get_config()
        scripts = []

        # Flatpickr initialization
        if config.get('use_flatpickr', True):
            scripts.append("""
            // Initialize Flatpickr date pickers
            document.querySelectorAll('.flatpickr-date').forEach(function(element) {
                flatpickr(element, {
                    dateFormat: element.dataset.dateFormat || 'Y-m-d',
                    allowInput: true
                });
            });

            document.querySelectorAll('.flatpickr-datetime').forEach(function(element) {
                flatpickr(element, {
                    enableTime: true,
                    dateFormat: element.dataset.dateFormat || 'Y-m-d H:i',
                    allowInput: true
                });
            });

            document.querySelectorAll('.flatpickr-time').forEach(function(element) {
                flatpickr(element, {
                    noCalendar: true,
                    enableTime: true,
                    dateFormat: element.dataset.dateFormat || 'H:i',
                    allowInput: true
                });
            });
            """)

        # Select2 initialization
        if config.get('use_select2', True):
            scripts.append("""
            // Initialize Select2 dropdowns
            $(document).ready(function() {
                $('.select2-single').select2({
                    theme: 'classic',
                    width: '100%',
                    allowClear: true
                });

                $('.select2-multiple').select2({
                    theme: 'classic',
                    width: '100%',
                    allowClear: true
                });
            });
            """)

        # Quill initialization
        if config.get('use_quill', True):
            scripts.append("""
            // Initialize Quill rich text editors
            document.querySelectorAll('.quill-editor').forEach(function(element) {
                const container = document.createElement('div');
                container.style.height = '200px';
                container.style.marginBottom = '1rem';
                element.style.display = 'none';
                element.parentNode.insertBefore(container, element);

                const quill = new Quill(container, {
                    theme: 'snow',
                    modules: {
                        toolbar: [
                            [{ 'header': [1, 2, 3, false] }],
                            ['bold', 'italic', 'underline', 'strike'],
                            ['blockquote', 'code-block'],
                            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                            [{ 'indent': '-1'}, { 'indent': '+1' }],
                            ['link', 'image'],
                            ['clean']
                        ]
                    }
                });

                // Sync Quill content to textarea
                quill.on('text-change', function() {
                    element.value = quill.root.innerHTML;
                });

                // Set initial content
                if (element.value) {
                    quill.root.innerHTML = element.value;
                }

                // Handle form submission
                const form = element.closest('form');
                if (form) {
                    form.addEventListener('submit', function() {
                        element.value = quill.root.innerHTML;
                    });
                }
            });
            """)

        if scripts:
            return f"<script>{' '.join(scripts)}</script>"

        return ""

    def customize_form_class(self, form_class, **kwargs):
        """Add custom form class modifications."""
        # Could add form validation, custom clean methods, etc.
        return form_class

    def ready(self):
        """Called after all plugins are loaded."""
        import logging
        logger = logging.getLogger(__name__)

        config = self.get_config()
        enabled_widgets = []

        if config.get('use_flatpickr', True):
            enabled_widgets.append('Flatpickr')
        if config.get('use_select2', True):
            enabled_widgets.append('Select2')
        if config.get('use_quill', True):
            enabled_widgets.append('Quill')

        logger.info(
            f"Advanced Widgets plugin v{self.version} ready. "
            f"Enabled widgets: {', '.join(enabled_widgets)}"
        )


# This allows the plugin to be discovered
SundaePlugin = AdvancedWidgetsPlugin