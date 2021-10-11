from django.urls import path

from main import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', views.BBLoginView.as_view(), name='login'),
    path('accounts/logout/', views.BBLogoutView.as_view(), name='logout'),
    path(
        'accounts/password/change/',
        views.BBPasswordChangeView.as_view(),
        name='password_change',
    ),
    path(
        'accounts/password/reset/complete/',
        views.BBPasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path(
        'accounts/password/reset/confirm/<uidb64>/<token>/',
        views.BBPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'accounts/password/reset/done/',
        views.BBPasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'accounts/password/reset/',
        views.BBPasswordResetView.as_view(),
        name='password_reset',
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
    path('<str:page>/', views.other_page, name='other'),
]
