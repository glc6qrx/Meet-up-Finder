from django.test import TestCase
from django.urls import reverse, resolve
from meetupfinder.views import index,events,profile,add_event


class TestUrls(TestCase):
    def test_index_url_is_resolved(self):
        url = reverse('meetupfinder:index')
        self.assertEquals(resolve(url).func, index)

    def test_events_url_is_resolved(self):
        url = reverse('meetupfinder:events')
        self.assertEquals(resolve(url).func, events)
    
    def test_events_url_is_resolved(self):
        url = reverse('meetupfinder:profile')
        self.assertEquals(resolve(url).func, profile)
    
    def test_events_url_is_resolved(self):
        url = reverse('meetupfinder:add_event')
        self.assertEquals(resolve(url).func, add_event)