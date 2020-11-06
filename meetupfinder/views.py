from django.shortcuts import render
from django.urls import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event
from .forms import EventFilterForm


def index(request):
    return render(request, 'meetupfinder/index.html')

def profile(request):
    return render(request, 'meetupfinder/profile.html')
    
def events(request):
    if not request.user.is_authenticated:    
        print("NOT")
        return HttpResponseRedirect(reverse('meetupfinder:index'))
    
    #if form submission, validate data and filter
    if request.method == 'POST':
        form = EventFilterForm(request.POST)
        if form.is_valid():
            events = Event.objects.all()
            #filter by name if provided
            name = form.cleaned_data['name']
            if name is not None:
                events = events.filter(event_name__icontains=name)
            #filter by start date if provided
            start_date = form.cleaned_data['start_date']
            if start_date is not None:
                events = events.filter(event_date__date__gte=start_date)
            #filter by end date if provided
            end_date = form.cleaned_data['end_date']
            if end_date is not None:
                events = events.filter(end_event_date__date__lte=end_date)
            #filter by categories if provided
            categoriesList = form.cleaned_data['category']
            if categoriesList:
                events = events.filter(category__id__in=categoriesList)
    
    #otherwise, create blank form
    else:
        form = EventFilterForm()
        events = Event.objects.all()
    
    return render(request, 'meetupfinder/events.html', {'title': 'Events', 'events': events, 'form': form})
