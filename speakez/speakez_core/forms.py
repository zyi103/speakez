from django.forms import ModelForm, Textarea
from .models import CallMessage, Category

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CallMessageForm(ModelForm):
    class Meta:
        model = CallMessage
        fields = ['duration', 'title', 'content', 'audio']
        widgets = {
            'content': Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )