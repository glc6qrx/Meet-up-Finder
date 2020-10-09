from django.urls import path
from . import views

app_name = 'meetupfinder'

urlpatterns = [
    path('', views.index, name='index')
]