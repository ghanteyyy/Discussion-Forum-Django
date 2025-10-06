from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('fetch-messages/', views.fetch_messages, name="fetch-messages"),

    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(
            template_name='reset_password/find_account.html',
            extra_context={'page_title': 'Reset Password | StockVault'},
            subject_template_name='registration/password_reset_subject.txt',
            email_template_name='registration/password_reset_email.txt',
            html_email_template_name='registration/password_reset_email.html'
        ),
        name='reset_password'
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='reset_password/reset_password_sent.html',
            extra_context={'page_title': 'Password Reset Sent | StockVault'}
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='reset_password/new_password.html',
            extra_context={'page_title': 'Enter New Password | StockVault'}
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='reset_password/recover_password_complete.html',
            extra_context={'page_title': 'Password Reset Complete | StockVault'}
        ),
        name='password_reset_complete'
    ),
]
