from django.test import TestCase
from meetupfinder.models import Event, Categories
from meetupfinder.views import index,events
from django.utils import timezone


class TestCategory(TestCase):
    def setUp(self):
        self.category1 = Categories.objects.create(
            cat_name = "Test Category"
        )
        self.category1.save()
    
    def tearDown(self):
        self.category1.delete()
    
    def test_category_created(self):
        category1 = Categories.objects.get(cat_name='Test Category')
        self.assertEquals(category1.cat_name, 'Test Category')


class TestEvent(TestCase):
    def setUp(self):
        self.currentDateTime = timezone.now()
        self.event1 = Event.objects.create(
            event_name='Event 1',
            event_text='Event text 1',
            event_date=self.currentDateTime,
            end_event_date=self.currentDateTime,
            event_host='Event host',
            address='Test Address',
            latitude=10,
            longitude=20
        )
        self.event1.save()

    def tearDown(self):
        self.event1.delete()
    
    def test_event_text_is_assigned_on_creation(self):
        event1 = Event.objects.get(event_name='Event 1')
        self.assertEquals(event1.event_name, 'Event 1')
        self.assertEquals(event1.event_text, 'Event text 1')
        self.assertEquals(event1.event_date, self.currentDateTime)
        self.assertEquals(event1.end_event_date, self.currentDateTime)
        self.assertEquals(event1.event_host, 'Event host')
        self.assertEquals(event1.address, 'Test Address')
        self.assertEquals(event1.latitude, 10)
        self.assertEquals(event1.longitude, 20)


class TestEventWithCategory(TestCase):
    def setUp(self):
        self.category1 = Categories.objects.create(
            cat_name = "Test Category"
        )
        self.category1.save()

        self.event1 = Event.objects.create(
            event_name='Event 1',
            category=self.category1
        )
        self.event1.save()

    def tearDown(self):
        self.event1.delete()
        self.category1.delete()
    
    def test_event_with_category(self):
        event1 = Event.objects.get(event_name='Event 1')
        self.assertEquals(event1.event_name, 'Event 1')
        self.assertEquals(event1.category.cat_name, 'Test Category')

