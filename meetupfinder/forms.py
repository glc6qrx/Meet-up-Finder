from django import forms
from .models import Categories

class EventFilterForm(forms.Form):
    name = forms.CharField(label='Event Name', max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    start_date = forms.DateField(label='Start Date', required=False, input_formats={'%m/%d/%y'},
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YY'}))

    end_date = forms.DateField(label='End Date', required=False, input_formats={'%m/%d/%y'},
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'MM/DD/YY'}))
        
    category = forms.ModelMultipleChoiceField(label="Categories (SHIFT-Click for multiple)", required=False,
    queryset=Categories.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))