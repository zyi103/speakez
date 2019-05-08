from django.test import TestCase
from .forms import CallMessageForm
from datetime import datetime, time, tzinfo

# Create your tests here.

class CallMessageCategoryFormsTest(TestCase):

    def test_valid_data(self):
        message_form = CallMessageForm({
            'date_time_created': time,
            'duration': 30,
            'title': "For Mom",
            'content': "Hi!",
        })
        self.assertTrue(message_form.is_valid())
        message = message_form.save()
        self.assertEqual(message.duration, 30)
        self.assertEqual(message.title, "For Mom")
        self.assertEqual(message.content, "Hi!")

    def test_blank_data(self):
        form = CallMessageForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'duration': ['This field is required.'],
            'title': ['This field is required.'],
        })