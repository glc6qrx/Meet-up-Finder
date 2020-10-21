from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    event_name= models.CharField(max_length=200)
    event_text= models.CharField(max_length=400)
    event_host= models.CharField(max_length=200)
    event_date= models.DateTimeField('event date')
    end_event_date= models.DateTimeField('end event date')
    def __str__(self):
       return self.event_text
# location -- text field or something else
# categories (own model)
