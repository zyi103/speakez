from django.forms import ModelForm, Textarea
from .models import CallMessage, Category

class CallMessageForm(ModelForm):
    class Meta:
        model = CallMessage
        fields = ['duration', 'title', 'content', 'audio']
        widgets = {
            'content': Textarea(attrs={'cols': 60, 'rows': 15}),
        }
