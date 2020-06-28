from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name='chat'

urlpatterns = [
    path('', views.all_conv, name='all_conv'),
    path('<str:room_name>/', views.room, name='room'),
    path('logout', views.logout, name='logout')
]