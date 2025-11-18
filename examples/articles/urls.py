from django.urls import path, include
from .views import ArticleView, AuthorView

urlpatterns = [
    path('', include(ArticleView.get_urls())),
    path('', include(AuthorView.get_urls())),
]