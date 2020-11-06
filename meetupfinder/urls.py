from django.urls import path
from . import views

app_name = 'meetupfinder'

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.events, name='events'),
    path('profile/', views.profile, name='profile'),
    path('attend/<int:event_id>/', views.attend, name='attend'),
    path('cancel_attendance/<int:event_id>/', views.cancel_attendance, name='cancel_attendance')
]