from django.shortcuts import render, get_object_or_404
from django.urls import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect
from .models import Event
from .forms import EventFilterForm, AddEventForm
from datetime import datetime
from places.fields import PlacesField
from json import dumps
import requests, math, decimal


def index(request):
    return render(request, 'meetupfinder/index.html')

def profile(request):
    attending_events = request.user.attending_events.all()
    return render(request, 'meetupfinder/profile.html', {'attending_events': attending_events})
    
def events(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('meetupfinder:index'))
    
    events = Event.objects.order_by('-event_date')
    
    #if form submission, validate data and filter
    if request.method == 'POST':
        form = EventFilterForm(request.POST)
        if form.is_valid():
            #filter by name if provided
            name = form.cleaned_data['name']
            if name is not "":
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
            #filter by distance range if range and user location provided
            location = form.cleaned_data['location']
            form_range = form.cleaned_data['distance']
            if location is not "" and form_range is not None:
                api_key = "AIzaSyCf4vECJyy-z-pq7NV93fpwP5hlZYs8pmo"
                r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}")
                user_lat = r.json()["results"][0]["geometry"]["location"]["lat"]
                user_lon = r.json()["results"][0]["geometry"]["location"]["lng"]
                # if an event is farther away from the user than the specified range, remove it from results
                for event in events:
                    if calculateDistance(event.latitude, event.longitude, user_lat, user_lon) > form_range:
                        events = events.exclude(id=event.id)
    
    #otherwise, create blank form
    else:
        form = EventFilterForm()
        
    #create location information for map
    locations = []
    for event in events:
        locations.append([event.event_name, event.address, float(event.latitude), float(event.longitude)])
    locationData = dumps({'locations': locations})
    
    return render(request, 'meetupfinder/events.html', {'title': 'Events', 'events': events, 
    'locationData': locationData, 'form': form})


#helper function to find distance (in miles) between two lat-long points using Law of Cosines
def calculateDistance(lat1, lng1, lat2, lng2):
	φ1 = decimal.Decimal(lat1) * decimal.Decimal(math.pi/180)
	φ2 = decimal.Decimal(lat2) * decimal.Decimal(math.pi/180)
	Δλ = (decimal.Decimal(lng2)-decimal.Decimal(lng1)) * decimal.Decimal(math.pi/180)
	R = 6371
	dKm = math.acos( math.sin(φ1)*math.sin(φ2) + math.cos(φ1)*math.cos(φ2) * math.cos(Δλ) ) * R
	distMI = dKm * 0.539957 #km to miles
	return distMI


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
            address = form.cleaned_data['address']

            #process the date and time info
            start_date = datetime(date.year, date.month, date.day, 
                start_time.hour, start_time.minute)
            end_date = datetime(date.year, date.month, date.day,
                end_time.hour, end_time.minute)
            
            #process address data with Google Maps Geocoding API
            api_key = "AIzaSyCf4vECJyy-z-pq7NV93fpwP5hlZYs8pmo"
            r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}")
            latitude = r.json()["results"][0]["geometry"]["location"]["lat"]
            longitude = r.json()["results"][0]["geometry"]["location"]["lng"]

            #create and save the new event to the database
            event = Event(event_name=name, event_text=description, event_host=host, event_date=start_date,
            end_event_date=end_date, category=category, address=address, latitude=latitude, longitude=longitude)
            event.save()
            return HttpResponseRedirect(reverse('meetupfinder:events'))
        
    #otherwise, create blank form
    else:
        form = AddEventForm()
    
    return render(request, 'meetupfinder/add_event.html', {'title': 'Add Event', 'form': form})

