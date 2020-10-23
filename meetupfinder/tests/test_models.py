from django.test import TestCase
from meetupfinder.models import Event
from meetupfinder.views import index,events
from django.utils import timezone


# Create your tests here.
class DummyTestCase(TestCase):
    def setUp(self):
        self.x = 1

    def test_dummy_test_case(self):
        self.assertEqual(self.x, 1)

class TestEvent(TestCase):
    
    def setUp(self):
        self.event1 = Event.objects.create(
            event_name='Event 1',
            event_text='Event text 1'
        )
        self.event1.save()

    def tearDown(self):
        self.event1.delete()
    
    def test_event_text_is_assigned_on_creation(self):
        #self.assertEquals(self.event1.event_name, 'Event 1')
        #self.assertEquals(self.event1.event_text, 'Event text 1')
        event1 = Event.objects.get(event_name='Event 1')
        self.assertEquals(event1.event_name, 'Event 1')
        self.assertEquals(event1.event_text, 'Event text 1')


    #def test_event_text(self):
        #text = Event(event_text='event text stuff')
        #self.assertEqual(str(text), text.event_text)