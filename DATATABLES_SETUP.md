# DataTables Plugin - Setup and Usage

## What Was Needed

The DataTables plugin is now **fully configured and enabled**. Here's what was required to make it work:

### 1. Fixed CSS Framework Conflict ✅

**Problem**: The plugin was using Bootstrap 5 styling, but the app uses Tailwind CSS. These frameworks conflict.

**Solution**: Switched to default DataTables styling:
```python
# Before (Bootstrap)
'https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css'
'https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js'

# After (Default + Tailwind)
'https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css'
# No Bootstrap JS integration needed
```

### 2. Plugin Registration ✅

The plugin is already registered and active:
```python
# In examples/articles/sundae_plugin.py
datatables_plugin = DataTablesPlugin()
registry.register('sundae_datatables', datatables_plugin)
```

### 3. Configuration in Settings ✅

Already configured in `examples/demo/settings.py`:
```python
SUNDAE_PLUGINS = {
    'config': {
        'sundae_datatables': {
            'page_length': 25,
            'responsive': True,
            'dom': 'Bfrtip',
            'buttons': ['copy', 'csv', 'excel', 'pdf', 'print'],
            'order': [[0, 'asc']],
        },
    }
}
```

### 4. Template Integration ✅

The base template already has:
- `{% load sundae_plugin_tags %}` - Loads plugin template tags
- `{% plugin_static_css %}` - Includes DataTables CSS
- `{% plugin_static_js %}` - Includes DataTables JavaScript
- `{% plugin_hook "body_end" %}` - Runs initialization script

### 5. Table Markup ✅

The list template has the correct table class:
```html
<table class="table-admin">
```

DataTables looks for this class to initialize.

## What You Should See

When you visit the article list page at `/article/`, you should see:

### 1. **Enhanced Table Features**
- **Search box** at top right - filter/search all columns
- **Entries dropdown** at top left - change number of rows per page
- **Pagination controls** at bottom - navigate through pages
- **Sorting** - click column headers to sort

### 2. **Export Buttons**
At the top of the table:
- **Copy** - Copy table data to clipboard
- **CSV** - Download as CSV file
- **Excel** - Download as Excel file
- **PDF** - Download as PDF file
- **Print** - Print-friendly view

### 3. **Responsive Design**
On smaller screens, columns automatically collapse with expand/collapse icons.

### 4. **Styling**
- Clean Tailwind styling integrated with DataTables
- Matches the rest of the application design
- Professional look with proper spacing and borders

## How It Works

### Auto-Detection
```python
# When ArticleView renders the list
view.template_name_suffix = '_list'  # DataTables detects this

# Plugin adds to context
context['datatables_enabled'] = True
context['datatables_config'] = { ... }
```

### Initialization
```javascript
// Automatically injected at body_end
$(document).ready(function() {
    $('.table-admin').DataTable({
        pageLength: 25,
        responsive: true,
        dom: 'Bfrtip',
        buttons: ['copy', 'csv', 'excel', 'pdf', 'print']
    });
});
```

## Verification

To verify DataTables is working, check the browser console:

1. **Open DevTools** (F12)
2. **Check Console** - Should have no DataTables errors
3. **Check Network Tab** - Should see:
   - `jquery.dataTables.min.css` loaded
   - `jquery.dataTables.min.js` loaded
   - `dataTables.buttons.min.js` loaded

4. **Check Elements** - The table should be wrapped in:
   ```html
   <div class="dataTables_wrapper">
       <div class="dataTables_filter">...</div>
       <table class="table-admin dataTable">...</table>
       <div class="dataTables_paginate">...</div>
   </div>
   ```

## Testing Export Buttons

### CSV/Excel Export
1. Click **CSV** or **Excel** button
2. File should download immediately
3. Open file - should contain all table data

### PDF Export
1. Click **PDF** button
2. PDF should download with formatted table
3. Requires pdfmake library (already loaded)

### Copy
1. Click **Copy** button
2. Should show "Copied to clipboard" message
3. Paste (Ctrl+V) - should paste table data

### Print
1. Click **Print** button
2. Opens print dialog with formatted table
3. Can save as PDF or print to printer

## Customization

### Change Page Length
```python
# In settings.py
'sundae_datatables': {
    'page_length': 50,  # Show 50 rows per page
}
```

### Disable Buttons
```python
'sundae_datatables': {
    'buttons': ['copy', 'csv'],  # Only copy and CSV
}
```

### Change Sort Order
```python
'sundae_datatables': {
    'order': [[1, 'desc']],  # Sort by 2nd column descending
}
```

### Disable for Specific View
```python
class ArticleView(CRUDSundaeView):
    skip_hooks = ['filter_list_context']  # Disable DataTables
```

## Troubleshooting

### DataTables Not Showing

**Check 1**: Open DevTools Console
```
Error: DataTables is not a function
→ jQuery or DataTables JS not loaded
```

**Check 2**: Inspect table element
```html
<!-- Should be table-admin not something else -->
<table class="table-admin">
```

**Check 3**: Check context in view
```python
python manage.py shell
>>> from articles.views import ArticleView
>>> # Check datatables_enabled in context
```

### Export Buttons Not Working

**Check**: Are required libraries loaded?
- JSZip (for Excel)
- pdfmake (for PDF)

These are automatically included by the plugin.

### Styling Issues

**Issue**: DataTables looks unstyled
**Solution**: Check CSS is loaded in `<head>`
```html
<link href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
```

## Disabling DataTables

### For All Views
```python
# In settings.py
SUNDAE_PLUGINS = {
    'disabled': ['sundae_datatables'],
}
```

### For One View
```python
class ArticleView(CRUDSundaeView):
    enable_plugins = False  # Disable all plugins
    # OR
    skip_hooks = ['filter_list_context']  # Disable just DataTables
```

## Summary

✅ **Plugin is enabled and configured**
✅ **CSS framework conflict resolved**
✅ **Template integration complete**
✅ **Should work on article list page**

Just refresh your browser and DataTables should be active on `/article/`!
