# Quill Text Editor Integration Demo

## Overview

The demo application now uses the Quill rich text editor for the Article content field, automatically applied via the Advanced Widgets plugin system.

## How It Works

### 1. Plugin Auto-Discovery

The `AdvancedWidgetsPlugin` is automatically discovered from `examples/articles/sundae_plugin.py` when Django starts.

### 2. Widget Customization

When creating a form, the plugin:

1. **Detects TextField widgets** - Checks if the field is a TextField
2. **Matches field names** - Looks for fields with names like 'content', 'body', 'description', 'text', 'html'
3. **Applies Quill widget** - Adds the `quill-editor` class and appropriate attributes

```python
# From sundae_plugin_widgets.py
if field_type == 'TextField':
    rich_text_fields = config.get('rich_text_fields', [
        'content', 'body', 'description', 'text', 'html'
    ])

    if any(rtf in field_name.lower() for rtf in rich_text_fields):
        widgets[field_name] = forms.Textarea(attrs={
            'class': 'form-control quill-editor',
            'rows': 10,
        })
```

### 3. JavaScript Initialization

The plugin automatically:

1. **Includes Quill CSS** - `https://cdn.quilljs.com/1.3.6/quill.snow.css`
2. **Includes Quill JS** - `https://cdn.quilljs.com/1.3.6/quill.js`
3. **Initializes editors** - Finds all `.quill-editor` elements and converts them

```javascript
// Automatically injected at body_end
document.querySelectorAll('.quill-editor').forEach(function(element) {
    const container = document.createElement('div');
    container.style.height = '200px';
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
                ['link', 'image'],
                ['clean']
            ]
        }
    });

    // Sync content to hidden textarea
    quill.on('text-change', function() {
        element.value = quill.root.innerHTML;
    });
});
```

## Configuration

The Quill editor is configured in `examples/demo/settings.py`:

```python
SUNDAE_PLUGINS = {
    'config': {
        'sundae_advanced_widgets': {
            'use_quill': True,  # Enable Quill
            'rich_text_fields': ['content', 'body', 'description', 'text', 'html'],
        },
    }
}
```

## Testing

### Verify Widget Applied

```python
from articles.views import ArticleView
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/article/create/')

view = ArticleView()
view.request = request
view.setup(request)

form = view.get_form_class()()
content_widget = form.fields['content'].widget

print(content_widget.__class__.__name__)  # Textarea
print(content_widget.attrs)  # {'class': 'form-control quill-editor', 'rows': 10}
```

### Verify Files Loaded

```python
from sundae.plugins.registry import PluginRegistry

css_files = PluginRegistry.execute_hook('get_css_files')
js_files = PluginRegistry.execute_hook('get_js_files')

# Should include:
# - https://cdn.quilljs.com/1.3.6/quill.snow.css
# - https://cdn.quilljs.com/1.3.6/quill.js
```

## Features

The Quill editor provides:

- **Rich formatting**: Bold, italic, underline, strike-through
- **Headers**: H1, H2, H3
- **Lists**: Ordered and bullet lists
- **Blockquotes & code blocks**
- **Links and images**
- **Clean formatting** button
- **HTML output**: Saved as HTML to the TextField

## Zero Configuration Required

The best part? **No code changes needed!**

Just:
1. ✅ Plugin is in the app directory
2. ✅ App is in INSTALLED_APPS
3. ✅ Field name contains 'content'
4. ✅ Field is a TextField

The Quill editor is automatically applied!

## Disabling

To disable Quill for the demo:

```python
# In settings.py
SUNDAE_PLUGINS = {
    'config': {
        'sundae_advanced_widgets': {
            'use_quill': False,  # Disable Quill
        },
    }
}
```

Or disable the entire plugin:

```python
SUNDAE_PLUGINS = {
    'disabled': ['sundae_advanced_widgets'],
}
```

## Other Fields Automatically Enhanced

The plugin also enhances:

- **DateField** → Flatpickr date picker
- **DateTimeField** → Flatpickr date/time picker
- **ForeignKey** → Select2 dropdown
- **ManyToManyField** → Select2 multi-select
- **ChoiceField** (small) → Radio buttons
- **ChoiceField** (large) → Enhanced select

All automatically, with zero configuration!
