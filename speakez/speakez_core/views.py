from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Refugee, Category, CallMessage

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, template_name='admin.html')


def list_recipients(request):
    recipients = Refugee.objects.all()
    return render(request, 'refugee/list.html', context={"refugees": recipients})
    

def list_call_messages(request):
    call_messages = CallMessage.objects.all()
    return render(request, 'refugee/messages.html', context={"messages": call_messages})
