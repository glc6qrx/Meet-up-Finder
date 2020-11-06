from django.contrib import admin

# Register your models here.
from .models import Event, Categories

admin.site.register(Event)
admin.site.register(Categories)