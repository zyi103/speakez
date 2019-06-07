from django.forms import ModelForm, Textarea, CheckboxSelectMultiple
from .models import CallMessage, Category, Refugee

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit



class CallMessageForm(ModelForm):
    class Meta:
        model = CallMessage
        fields = ['duration', 'title', 'category','content', 'audio']
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

class RefugeeForm(ModelForm):
    class Meta:
        model = Refugee
        fields = ('first_name','middle_name','last_name','gender','age','phone_number','demographic_info','ethnicity',
        'street_number','street_name','city','zip_code','emergency_contact','martial_status')
        
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        