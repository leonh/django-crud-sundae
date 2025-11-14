# Django CRUD Sundae Examples

This directory contains example implementations showing how to use django-crud-sundae in your Django projects.

## Installation

First, install django-crud-sundae:

```bash
pip install django-crud-sundae
```

Or install from the repository in development mode:

```bash
pip install -e /path/to/django-crud-sundae
```

## Using Sundae Views

Add `sundae` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'sundae',
    ...
]
```

Then use the Sundae views in your Django app:

```python
from sundae.views import (
    SundaeListView,
    SundaeDetailView,
    SundaeCreateView,
    SundaeUpdateView,
    SundaeDeleteView,
)
from .models import Article

class ArticleListView(SundaeListView):
    model = Article
    template_name = 'articles/article_list.html'

class ArticleDetailView(SundaeDetailView):
    model = Article
    template_name = 'articles/article_detail.html'

class ArticleCreateView(SundaeCreateView):
    model = Article
    fields = ['title', 'content', 'author']
    success_url = '/articles/'

class ArticleUpdateView(SundaeUpdateView):
    model = Article
    fields = ['title', 'content']
    success_url = '/articles/'

class ArticleDeleteView(SundaeDeleteView):
    model = Article
    success_url = '/articles/'
```

## Features

- **Tailwind CSS**: Pre-integrated with Tailwind CSS for modern styling
- **HTMX**: Built-in HTMX support for dynamic interactions
- **Django CBVs**: Extends Django's class-based views with additional functionality
- **Customizable**: Easy to override and extend for your specific needs

## Example Projects

More detailed example projects will be added here showing:
- Basic CRUD operations
- HTMX integration patterns
- Custom template overrides
- Advanced filtering and pagination
