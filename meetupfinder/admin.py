from django.contrib import admin
from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

# Register your models here.
from .models import Event, Categories


admin.site.register(Categories)

@admin.register(Event)
#class EventAdmin(OSMGeoAdmin):
#    list_display = ('event_name', 'location')

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_text')
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }