from django.shortcuts import render
from django.urls import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event


def index(request):
    return render(request, 'meetupfinder/index.html')


def events(request):
    if not request.user.is_authenticated:    
        print("NOT")
        return HttpResponseRedirect(reverse('meetupfinder:index'))
    
    events = Event.objects.all()
    return render(request, 'meetupfinder/events.html', {'title': 'Events', 'events': events})
