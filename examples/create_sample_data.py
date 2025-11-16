#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')
django.setup()

from articles.models import Article

# Clear existing articles
Article.objects.all().delete()

# Create sample articles
articles = [
    {
        'title': 'Getting Started with Django',
        'content': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.',
        'status': 'published'
    },
    {
        'title': 'Introduction to CRUD Operations',
        'content': 'CRUD stands for Create, Read, Update, and Delete. These are the four basic operations that can be performed on data in a database. Understanding CRUD is fundamental to building web applications.',
        'status': 'published'
    },
    {
        'title': 'Working with Django Models',
        'content': 'A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you are storing. Generally, each model maps to a single database table.',
        'status': 'published'
    },
    {
        'title': 'Django Views Explained',
        'content': 'A view function, or view for short, is a Python function that takes a web request and returns a web response. This response can be the HTML contents of a web page, or a redirect, or a 404 error, or an XML document, or an image.',
        'status': 'draft'
    },
    {
        'title': 'Understanding Django Templates',
        'content': 'The template layer provides a designer-friendly syntax for rendering the information to be presented to the user. Learn how templates can inherit from other templates and how you can customize the rendering.',
        'status': 'draft'
    },
    {
        'title': 'Django URL Routing',
        'content': 'To design URLs for an app, you create a Python module informally called a URLconf (URL configuration). This module is pure Python code and is a mapping between URL path expressions to Python functions.',
        'status': 'published'
    },
    {
        'title': 'Django Forms Tutorial',
        'content': 'Django provides a powerful form library that handles rendering forms as HTML, validating user-submitted data, and converting that data to native Python types. Forms are a very powerful and flexible system for collecting user input.',
        'status': 'published'
    },
    {
        'title': 'Database Migrations in Django',
        'content': 'Migrations are Django\'s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. They are designed to be mostly automatic, but you will need to know when to make migrations.',
        'status': 'published'
    },
]

for article_data in articles:
    Article.objects.create(**article_data)

print(f"Created {len(articles)} sample articles")
print(f"Total articles in database: {Article.objects.count()}")
