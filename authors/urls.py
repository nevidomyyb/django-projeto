from django.urls import path

from . import views

app_name = 'authors'
urlpatterns = [
    path('register/', views.registerview, name='register'),
    path('register/create/', views.registercreate, name='create'),
]
