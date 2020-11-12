from django.shortcuts import render, get_object_or_404
from django.urls import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event
from .forms import EventFilterForm, AddEventForm, EventMapForm
from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from datetime import datetime


longitude = -80.191788
latitude = 25.761681

user_location = Point(longitude, latitude, srid=4326)

class Home(generic.ListView):
    model = Event


    fields = ('lat', 'lon')
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.point = fromstr('POINT(%s %s)'%(self.object.lon, self.object.lat), srid=4326)
        self.object.save()
        return redirect('member:all_members')


    context_object_name = 'events'
    queryset = Event.objects.annotate(distance=Distance('location',
    user_location)
    ).order_by('distance')[0:6]
    template_name = 'meetupfinder/events.html'



def index(request):
    return render(request, 'meetupfinder/index.html')

def profile(request):
    attending_events = request.user.attending_events.all()
    return render(request, 'meetupfinder/profile.html', {'attending_events': attending_events})
    
def events(request):
    if not request.user.is_authenticated:
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


def attend(request, event_id):
    if request.method == 'POST' and request.user.is_authenticated:
        event = get_object_or_404(Event, pk=event_id)
        event.attending_users.add(request.user)
        event.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(reverse('meetupfinder:index'))


def cancel_attendance(request, event_id):
    if request.method == 'POST' and request.user.is_authenticated:
        event = get_object_or_404(Event, pk=event_id)
        event.attending_users.remove(request.user)
        event.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(reverse('meetupfinder:index'))


def add_event(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('meetupfinder:index'))
    
    #if form submission, validate data and filter
    if request.method == 'POST':
        form = AddEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            host = form.cleaned_data['host']
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            category = form.cleaned_data['category']

            #process the date and time info
            start_date = datetime(date.year, date.month, date.day, 
                start_time.hour, start_time.minute)
            end_date = datetime(date.year, date.month, date.day,
                end_time.hour, end_time.minute)

            #create and save the new event to the database
            event = Event(event_name=name, event_text=description, event_host=host, event_date=start_date,
            end_event_date=end_date, category=category)
            event.save()
            return HttpResponseRedirect(reverse('meetupfinder:events'))
        
    #otherwise, create blank form
    else:
        form = AddEventForm()
    
    return render(request, 'meetupfinder/add_event.html', {'title': 'Add Event', 'form': form})

