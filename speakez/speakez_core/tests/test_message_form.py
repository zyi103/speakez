# from django.test import TestCase
# from ..forms import CallMessageForm
# from ..models import CallMessage
# from django.utils import timezone
# from datetime import datetime, time, tzinfo
# from django.core.files.uploadedfile import SimpleUploadedFile
# # Create your tests here.

# import os 
# dir_path = os.path.dirname(os.path.realpath(__file__))

# class CallMessageFormTest(TestCase):

#     def test_valid_data(self):
#         with open(os.path.join(dir_path, 'organfinale.wav'), 'rb') as file:
#             myGoodfile = SimpleUploadedFile("testfile.wav", file.read(), content_type="audio/wav")
#             message_form = CallMessageForm({
#                 'duration': 30,
#                 'title': "For Mom",
#                 'content': "Hi!"
#             }, 
#             {
#                 "audio": myGoodfile
#             }
#             )
#             self.assertTrue(message_form.is_valid())
#             message = message_form.save()
#             self.assertEqual(message.duration, 30)
#             self.assertEqual(message.title, "For Mom")
#             self.assertEqual(message.content, "Hi!")

#         with open(os.path.join(dir_path, 'test.pdf'), 'rb') as file:
#             myBadfile = SimpleUploadedFile("testfile.pdf", file.read(), content_type="application/pdf")
#             bad_message_form = CallMessageForm({
#                 'duration': 30,
#                 'title': "For Mom",
#             }, 
#             {
#                 "audio": myBadfile
#             }
#             )
#             self.assertFalse(bad_message_form.is_valid())
#             self.assertEqual(bad_message_form.errors, {
#                 'audio': ["File extension 'pdf' is not allowed. Allowed extensions are: 'wav'."]
#             })



#     def test_blank_data(self):
#         form = CallMessageForm({})
#         self.assertFalse(form.is_valid())
#         self.assertEqual(form.errors, {
#             'duration': ['This field is required.'],
#             'title': ['This field is required.'],
#         })