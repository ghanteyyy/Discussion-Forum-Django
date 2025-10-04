from django.urls import path, include
from . import views


urlpatterns = [
    path('users/', views.AdminPage, name='admin-home'),
    path('user/add', views.AddUser, name='admin-user-add'),
    path('user/edit', views.EditUser, name='admin-user-edit'),
    path('user/delete', views.DeleteUser, name='admin-user-delete'),

    path('rooms/', views.RoomsPage, name='admin-rooms'),
    path('topics/', views.TopicsPage, name='admin-topics'),
    path('messages/', views.MessagesPage, name='admin-messages'),
]
