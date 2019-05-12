from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Refugee, Category, CallMessage
from .forms import CallMessageForm
import pdb;

@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, template_name='admin.html')


def list_recipients(request):
    recipients = Refugee.objects.all()
    return render(request, 'refugee/list.html', context={"refugees": recipients})
    
def edit_messages(request):
    # pdb.set_trace()
    form = CallMessageForm(request.POST, request.FILES)
    if form.is_valid(): 
        print("valid")
        form.save()
    else:
        print("not valid")

    # if request.method == 'POST':
    #     uploaded_audio = request.FILES['']

    return render(request, 'message/message-list.html', context = {"form" : form})
    

def list_call_messages(request):
    ordered_call_messages = CallMessage.objects.order_by('-date_time_created')
    return render(request, 'refugee/messages.html', context={"messages": ordered_call_messages})


def call_message_detail(request, call_message_id):
    call_message = get_object_or_404(CallMessage, pk=call_message_id)
    return render(request, 'refugee/message_detail.html', context={"message": call_message})
