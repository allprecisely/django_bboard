from django.urls import path

from api import views

app_name = 'api'
urlpatterns = [
    path('bbs/<int:pk>/comments/', views.comments, name='comments'),
    path('bbs/<int:pk>/', views.BbDetailView.as_view(), name='detail'),
    path('bbs/', views.bbs, name='bbs'),
]
