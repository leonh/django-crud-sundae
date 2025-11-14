"""
Example views using Django CRUD Sundae

This file demonstrates how to use the sundae views in your Django project.
"""

from sundae.views import (
    SundaeListView,
    SundaeDetailView,
    SundaeCreateView,
    SundaeUpdateView,
    SundaeDeleteView,
)

# Assuming you have a model like this:
#
# from django.db import models
#
# class Article(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     author = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.title
#
#     def get_absolute_url(self):
#         return f"/articles/{self.pk}/"


class ArticleListView(SundaeListView):
    """List all articles."""
    # model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10


class ArticleDetailView(SundaeDetailView):
    """Display a single article."""
    # model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'


class ArticleCreateView(SundaeCreateView):
    """Create a new article."""
    # model = Article
    fields = ['title', 'content', 'author']
    template_name = 'articles/article_form.html'
    success_url = '/articles/'


class ArticleUpdateView(SundaeUpdateView):
    """Update an existing article."""
    # model = Article
    fields = ['title', 'content']
    template_name = 'articles/article_form.html'
    success_url = '/articles/'


class ArticleDeleteView(SundaeDeleteView):
    """Delete an article."""
    # model = Article
    template_name = 'articles/article_confirm_delete.html'
    success_url = '/articles/'


# Example with custom context data
class ArticleListWithStatsView(SundaeListView):
    """List view with additional context."""
    # model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add custom context
        # context['total_articles'] = Article.objects.count()
        # context['recent_articles'] = Article.objects.order_by('-created_at')[:5]
        return context
