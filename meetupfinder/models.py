from django.db import models
from django.utils import timezone

# Create your models here.
class Event(models.Model):
   event_text= models.CharField(max_length=200)
   event_date= models.DateTimeField('event date')
   def __str__(self):
       return self.event_text