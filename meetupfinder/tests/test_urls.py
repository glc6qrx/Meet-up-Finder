from django.test import TestCase
from django.urls import reverse, resolve
from meetupfinder.views import index,events


class TestUrls(TestCase):

    def test_index_url_is_resolved(self):
        url = reverse('meetupfinder:index')
        self.assertEquals(resolve(url).func, index)

    def test_events_url_is_resolved(self):
        url = reverse('meetupfinder:events')
        self.assertEquals(resolve(url).func, events)