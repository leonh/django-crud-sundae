# django-crud-sundae

A useful view class for creating CRUD views in Django (With Tailwind & HTMX). Following the ice-cream metaphor established by Django Neapolitan and Django Vanilla views. This offers a few extras: a banana, squirt of cream and a drizzle of chocolate sauce!

## Installation

Install from PyPI (once published):

```bash
pip install django-crud-sundae
```

Or install from source:

```bash
git clone https://github.com/leonh/django-crud-sundae.git
cd django-crud-sundae
pip install -e .
```

## Quick Start

1. Add `sundae` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'sundae',
    ...
]
```

2. Use the Sundae views in your Django app:

```python
from sundae.views import SundaeListView, SundaeDetailView, SundaeCreateView
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
```

3. Wire up your URLs:

```python
from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCreateView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
]
```

## Features

- **Built on Django CBVs**: Extends Django's proven class-based views
- **Tailwind CSS Ready**: Pre-integrated base templates with Tailwind CSS
- **HTMX Support**: Built with HTMX patterns in mind for dynamic interactions
- **Simple & Extensible**: Easy to customize and override for your specific needs

## Available Views

- `SundaeListView` - For listing objects
- `SundaeDetailView` - For displaying a single object
- `SundaeCreateView` - For creating new objects
- `SundaeUpdateView` - For updating existing objects
- `SundaeDeleteView` - For deleting objects

## Examples

Check out the `examples/` directory for more detailed usage examples.

## Requirements

- Python 3.8+
- Django 3.2+

## License

MIT License - see LICENSE file for details.    
