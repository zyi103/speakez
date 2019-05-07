from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Refugee

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, template_name='admin.html')


def list_recipients(request):
    recipients = Refugee.objects.all()
    return render(request, 'refugee/list.html', context={"refugees": recipients})
    
def list_messages(request):
    return render(request, 'message/message-list.html')
    
