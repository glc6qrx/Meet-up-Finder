from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point

# Create your models here.
# categories (own model)
class Categories(models.Model):
    cat_name= models.CharField(max_length=200)
    def __str__(self):
       return self.cat_name

class Event(models.Model):
    event_name= models.CharField(max_length=200)
    event_text= models.CharField(max_length=400)
    event_host= models.CharField(max_length=200)
    event_date= models.DateTimeField('event date', null=True, blank=True)
    end_event_date= models.DateTimeField('end event date', null=True, blank=True)
    category = models.ForeignKey(Categories, null=True, blank=True, on_delete=models.CASCADE)
    attending_users = models.ManyToManyField(User, related_name='attending_events', blank=True)
    

    lat = models.FloatField(min_value=-90, max_value=90)
    lon = models.FloatField(min_value=-180, max_value=180)

    @property
    def lon(self):
        return self.location.x
    
    @property
    def lat(self):
        return self.location.y

    place = geos.Point(data['lng'], data['lat'], srid=4326)

    location = models.PointField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)

    mpoly = models.MultiPolygonField(null=True, blank=True)

    def __str__(self):
       return self.event_text
# location -- text field or something else
