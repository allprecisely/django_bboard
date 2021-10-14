from django.urls import path
# from django.views.decorators.cache import cache_page

from main import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.ArticleLoginView.as_view(), name='login'),
    path('accounts/logout/', views.ArticleLogoutView.as_view(), name='logout'),
    path(
        'accounts/password/change/',
        views.ArticlePasswordChangeView.as_view(),
        name='password_change',
    ),
    path(
        'accounts/password/reset/complete/',
        views.ArticlePasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path(
        'accounts/password/reset/confirm/<uidb64>/<token>/',
        views.ArticlePasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'accounts/password/reset/done/',
        views.ArticlePasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'accounts/password/reset/',
        views.ArticlePasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'accounts/profile/change/<int:pk>/',
        views.profile_article_change,
        name='profile_article_change',
    ),
    path(
        'accounts/profile/delete/<int:pk>/',
        views.profile_article_delete,
        name='profile_article_delete',
    ),
    path('accounts/profile/add/', views.profile_article_add, name='profile_article_add'),
    path(
        'accounts/profile/<int:pk>/', views.profile_article_detail, name='profile_article_detail'
    ),
    path('accounts/profile/', views.profile, name='profile'),
    path(
        'accounts/profile/change/',
        views.ChangeUserInfoView.as_view(),
        name='profile_change',
    ),
    path(
        'accounts/profile/delete/',
        views.DeleteUserView.as_view(),
        name='profile_delete',
    ),
    path('accounts/register/', views.RegisterUserView.as_view(), name='register'),
    path(
        'accounts/register/activate/<str:sign>',
        views.user_activate,
        name='register_activate',
    ),
    path(
        'accounts/register/done/',
        views.RegisterDoneView.as_view(),
        name='register_done',
    ),
    path('<int:city_pk>/<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/', views.by_city, name='by_city'),
    # path('<int:pk>/', cache_page(60)(views.by_city), name='by_city'),
    path('<str:page>/', views.other_page, name='other'),
]
