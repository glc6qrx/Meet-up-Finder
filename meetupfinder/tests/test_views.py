from django.test import TestCase, Client
from django.urls import reverse
from meetupfinder.models import Event, Categories
from meetupfinder.forms import AddEventForm, EventFilterForm
import json, requests
from django.contrib.auth.models import User
from urllib.parse import urlencode
from django.utils import timezone


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


class TestAddEventForm(TestCase):
    def setUp(self):
        self.category1 = Categories.objects.create(
            cat_name = "Test Category"
        )
        self.category1.save()
    
    def tearDown(self):
        self.category1.delete()

    def test_add_event_form_with_correct_data(self):
        self.form = AddEventForm(data={
            'name': 'Test Name',
            'description': 'Test Description',
            'host': 'Test Host',
            'date': '10/20/2020',
            'start_time': '10:30 AM',
            'end_time': '11:30 AM',
            'address': '1600 Amphitheatre Parkway, Mountain View, CA',
            'category': self.category1
        })
        self.assertTrue(self.form.is_valid)
    
    def test_add_event_form_with_no_data(self):
        self.form = AddEventForm(data={})
        self.assertEqual(self.form.errors['name'], ['This field is required.'])
        self.assertEqual(self.form.errors['description'], ['This field is required.'])
        self.assertEqual(self.form.errors['host'], ['This field is required.'])
        self.assertEqual(self.form.errors['date'], ['This field is required.'])
        self.assertEqual(self.form.errors['start_time'], ['This field is required.'])
        self.assertEqual(self.form.errors['end_time'], ['This field is required.'])
        self.assertEqual(self.form.errors['address'], ['This field is required.'])
        self.assertEqual(self.form.errors['category'], ['This field is required.'])
    
    def test_add_event_form_with_incorrect_date(self):
        self.form = AddEventForm(data={
            'name': 'Test Name',
            'description': 'Test Description',
            'host': 'Test Host',
            'date': 'abc',
            'start_time': '10:30 AM',
            'end_time': '11:30 AM',
            'address': '1600 Amphitheatre Parkway, Mountain View, CA',
            'category': self.category1
        })
        self.assertEqual(self.form.errors['date'], ['Enter a valid date.'])

    def test_add_event_form_with_incorrect_time(self):
        self.form = AddEventForm(data={
            'name': 'Test Name',
            'description': 'Test Description',
            'host': 'Test Host',
            'date': '10/20/20',
            'start_time': '10:30',
            'end_time': 'testing',
            'address': '1600 Amphitheatre Parkway, Mountain View, CA',
            'category': self.category1
        })
        self.assertEqual(self.form.errors['start_time'], ['Enter a valid time.'])
        self.assertEqual(self.form.errors['end_time'], ['Enter a valid time.'])


class TestAddressGeocoding(TestCase):
    def test_address_geocoding(self):
        self.address = "1600 Amphitheatre Parkway, Mountain View, CA"
        self.api_key = "AIzaSyCf4vECJyy-z-pq7NV93fpwP5hlZYs8pmo"
        self.r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?address={self.address}&key={self.api_key}")
        latitude = self.r.json()["results"][0]["geometry"]["location"]["lat"]
        longitude = self.r.json()["results"][0]["geometry"]["location"]["lng"]

        self.assertAlmostEqual(first=latitude, second=37.4267861, delta=0.01)
        self.assertAlmostEqual(first=longitude, second=-122.0806032, delta=0.01)


class TestFilterForm(TestCase):
    def setUp(self):
        self.currentDateTime = timezone.now()
        self.futureDateTime = self.currentDateTime + timezone.timedelta(hours=4)
        self.category1 = Categories.objects.create(
            cat_name = "Category One"
        )
        self.category1.save()
        self.category2 = Categories.objects.create(
            cat_name = "Category Two"
        )
        self.category2.save()
        self.event1 = Event.objects.create(
            event_name='Event 1',
            event_text='Event text 1',
            event_date=self.currentDateTime,
            end_event_date=self.futureDateTime,
            event_host='Event host',
            address='1600 Amphitheatre Parkway, Mountain View, CA',
            latitude=10,
            longitude=20,
            category = self.category1
        )
        self.event1.save()
        self.event2 = Event.objects.create(
            event_name='Event 2',
            event_text='Event text 2',
            event_date=self.currentDateTime,
            end_event_date=self.currentDateTime,
            event_host='Event host 2',
            address='1600 Amphitheatre Parkway, Mountain View, CA',
            latitude=30,
            longitude=40,
            category = self.category2
        )
        self.event2.save()
    
    def tearDown(self):
        self.category1.delete()
        self.category2.delete()
        self.event1.delete()
        self.event2.delete()
        
    def test_filter_form_with_name(self):
        self.form = EventFilterForm(data={
            'name': 'Event 1'
        })
        self.assertTrue(self.form.is_valid)
        if self.form.is_valid():
            events = Event.objects.all()
            events = events.filter(event_name__icontains=self.form.cleaned_data['name'])
            self.assertEquals(events.count(), 1)
            self.assertEquals(events.first(), self.event1)
    
    def test_filter_form_with_dates(self):
        self.form = EventFilterForm(data={
            'end_date': self.currentDateTime
        })
        self.assertTrue(self.form.is_valid)
        if self.form.is_valid():
            events = Event.objects.all()
            events = events.filter(end_event_date__date__lte=self.form.cleaned_data['end_date'])
            self.assertEquals(events.count(), 1)
            self.assertEquals(events.first(), self.event2)
        
    def test_filter_form_with_one_category(self):
        self.form = EventFilterForm(data={
            'category': {self.category1}
        })
        self.assertTrue(self.form.is_valid)
        if self.form.is_valid():
            events = Event.objects.all()
            events = events.filter(category__id__in=self.form.cleaned_data['category'])
            self.assertEquals(events.count(), 1)
            self.assertEquals(events.first(), self.event1)

    def test_filter_form_with_multiple_categories(self):
        self.form = EventFilterForm(data={
            'category': {self.category1, self.category2}
        })
        self.assertTrue(self.form.is_valid)
        if self.form.is_valid():
            events = Event.objects.all()
            events = events.filter(category__id__in=self.form.cleaned_data['category'])
            self.assertEquals(events.count(), 2)
    
    def test_filter_form_with_no_filters(self):
        self.form = EventFilterForm(data={})
        self.assertTrue(self.form.is_valid())
        if self.form.is_valid():
            events = Event.objects.all()
            self.assertEquals(events.count(), 2)


