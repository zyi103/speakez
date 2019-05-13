from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Refugee, Category, CallMessage
from .forms import CallMessageForm


@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, template_name='admin.html')


def list_recipients(request):
    recipients = Refugee.objects.all()
    return render(request, 'refugee/list.html', context={"refugees": recipients})
    
def edit_messages(request):
    form = CallMessageForm(request.POST, request.FILES)
    if form.is_valid(): 
        form.save()

    return render(request, 'message/edit_message.html', context = {"form" : form})
    

def list_call_messages(request):
    ordered_call_messages = CallMessage.objects.order_by('-date_time_created')
    return render(request, 'message/message_list.html', context={"messages": ordered_call_messages})


def call_message_detail(request, call_message_id):
    call_message = get_object_or_404(CallMessage, pk=call_message_id)
    return render(request, 'message/message_detail.html', context={"message": call_message})
