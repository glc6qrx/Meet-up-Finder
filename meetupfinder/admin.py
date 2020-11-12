from django.contrib import admin
from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
from .models import Event, Categories


admin.site.register(Categories)

@admin.register(Event)
class EventAdmin(OSMGeoAdmin):
    list_display = ('event_name', 'location')