from django.urls import path

from . import views

app_name = 'authors'
urlpatterns = [
    path('register/', views.registerview, name='register'),
    path('register/create/', views.registercreate, name='create'),

    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logoutAA, name='logout'),
    path('dashboard/', views.Dashboard, name='dashboard'),
]
