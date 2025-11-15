from django.urls import path, include
from .views import ArticleView

urlpatterns = [
    path('', include(ArticleView.get_urls())),
]