from django.test import TestCase
import json
import os


class TwilioCallback(TestCase):
    def test_twilio_callback(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path,'callback_result.json'),'rb') as f:
            request = json.load(f)
            print(request.keys())