from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('articles/<int:pk>/comments/', views.comments, name='comments'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('articles/', views.articles, name='articles'),
]
