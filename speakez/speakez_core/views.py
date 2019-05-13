from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Refugee, Category, CallMessage
from .forms import CallMessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.core.serializers.json import DjangoJSONEncoder



from speakez_core.forms import SignUpForm


@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, template_name='admin.html')


@login_required(login_url='/accounts/login/')
def list_recipients(request):
    recipients = Refugee.objects.all()
    return render(request, 'refugee/list.html', context={"refugees": recipients})


@login_required(login_url='/accounts/login/')
def edit_messages(request):
    form = CallMessageForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
    return render(request, 'message/edit_message.html', context={"form": form})


@login_required(login_url='/accounts/login/')
def list_call_messages(request):
    ordered_call_messages = CallMessage.objects.order_by('-date_time_created')
    return render(request, 'message/message_list.html', context={"messages": ordered_call_messages})


@login_required(login_url='/accounts/login/')
def call_message_detail(request, call_message_id):
    call_message = get_object_or_404(CallMessage, pk=call_message_id)
    return render(request, 'message/message_detail.html', context={"message": call_message})


@login_required(login_url='/accounts/login/')
@staff_member_required
def create_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('admin/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html',context={"form" : form})

@login_required(login_url='/accounts/login/')
def user_list(request):
    users = User.objects.all().values_list('username', 'email','first_name','last_name')
    users_json = json.dumps(list(users), cls=DjangoJSONEncoder)
    return render(request, 'registration/userlist.html',context={"users" : users_json})