from django.test import TestCase, Client
from django.urls import reverse
from meetupfinder.models import Event
import json
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('meetupfinder:index')
        self.events_url = reverse('meetupfinder:events')
        self.event1 = Event.objects.create(
            event_name='Event 1',
            event_text='Event text 1'
        )
        #self.user = User.objects.create_superuser(
        #    username="admin",
        #    password="adminadmin",
        #    email="admin@example.com"
        #)

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'meetupfinder/index.html')

    def test_events_GET(self):
        response = self.client.get(self.events_url, follow=True)
        response = self.client.post(self.events_url)
        self.assertEquals(response.status_code, 302)
        #self.client.force_login(self.user)
        #self.assertTemplateUsed(response, 'meetupfinder/events.html')

    #def test_events_POST(self):
    #    response = self.client.post(self.events_url)
    #    self.assertEquals(response.status_code, 302)