# from django.test import TestCase
# from ..forms import SignUpForm

# # Create your tests here.

# class UserFormTest(TestCase):

#     def test_valid_data(self):
#         user_form = SignUpForm({
#             'username': "test_user",
#             'email': "test@syr.edu",
#             'password1': "testpassword1",
#             'password2': "testpassword1"
#         })
#         self.assertTrue(user_form.is_valid())
#         user = user_form.save()
#         self.assertEqual(user.username, "test_user")
#         self.assertEqual(user.email, "test@syr.edu")
#         bad_user_form = SignUpForm({
#             'username': "test_user!",
#             'email': "test",
#             'password1': "testpassword1",
#             'password2': "testpassword2"
#         })
#         self.assertFalse(bad_user_form.is_valid())
#         self.assertEqual(bad_user_form.errors, {
#             'username': ["Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."],
#             'email': ["Enter a valid email address."],
#             'password2': ["The two password fields didn't match."]
#         })



#     def test_blank_data(self):
#         form = SignUpForm({})
#         self.assertFalse(form.is_valid())
#         self.assertEqual(form.errors, {
#             'username': ["This field is required."],
#             'email': ["This field is required."],
#             'password1': ["This field is required."],
#             'password2': ["This field is required."]
#         })