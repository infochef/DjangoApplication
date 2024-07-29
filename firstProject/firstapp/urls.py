from django.urls import path, include
from firstapp import views

urlpatterns = [
    path('', views.index, name='index'),#
    path('about/', views.about, name='about'),
    path('signup/', views.users, name='users'),
]