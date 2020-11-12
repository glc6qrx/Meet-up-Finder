from django import forms
from .models import Categories
from django.contrib.gis import forms

class EventFilterForm(forms.Form):
    name = forms.CharField(label='Event Name', max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    start_date = forms.DateField(label='Start Date', required=False, input_formats={'%m/%d/%y'},
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YY'}))

    end_date = forms.DateField(label='End Date', required=False, input_formats={'%m/%d/%y'},
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YY'}))
        
    category = forms.ModelMultipleChoiceField(label="Categories (SHIFT-Click for multiple)", required=False,
    queryset=Categories.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))



class AddEventForm(forms.Form):
    name = forms.CharField(label='Event Name', max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    description = forms.CharField(label='Description', max_length=400,
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    
    host = forms.CharField(label='Event Host', max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    date = forms.DateField(label='Date', input_formats={'%m/%d/%y'},
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YY'}))

    start_time = forms.TimeField(label='Start Time', input_formats={'%I:%M %p'},
        widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': '10:15 AM'}))
    
    end_time = forms.TimeField(label="End Time", input_formats={'%I:%M %p'},
        widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': '2:15 PM'}))
    
    lat = forms.CharField(label='Event Latitude', max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
        
    lon = forms.CharField(label='Event Longitude', max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    point = forms.PointField(label='Event Location', widget=
    forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))

    category = forms.ModelChoiceField(label="Category",
    queryset=Categories.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    

class EventMapForm(forms.Form):
    point = forms.PointField(widget=
    forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))