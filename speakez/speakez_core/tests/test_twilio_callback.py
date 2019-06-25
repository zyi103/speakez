from django.test import TestCase
import json
import os
from ..forms import CallStatusForm
import requests



class TwilioCallback(TestCase):
    def test_twilio_callback(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path,'callback_result.json'),'rb') as f:
            d = json.load(f)
            request = json.dumps(d)
        
        requests.post("http://127.0.0.1:8000/twilio/call_status_event/", data=request)
