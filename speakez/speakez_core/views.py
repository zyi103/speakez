from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Refugee, Category, CallMessage
from .forms import CallMessageForm, RefugeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.admin.views.decorators import staff_member_required

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from speakez_core.forms import SignUpForm

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated   
from .serializers import UserSerializer, NewUserSerializer, ChangePasswordSerializer
from .forms import CallMessageForm
from django.views.generic.edit import FormView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

class UserList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_list.html'

    def get(self, request):
        queryset = User.objects.all().order_by('-date_joined')
        return Response({'users': queryset})


class UserDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/user_detail.html'
    lookup_field = 'username'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, context = {'request': request})
        return Response({'serializer': serializer, 'user': user})

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user, data=request.data, context = {'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'user': user})
        serializer.save()
        return redirect('user_list')


class NewUser(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/new_user.html'

    def get(self, request):
        serializer = NewUserSerializer(context = {'request': request})
        return Response({'serializer': serializer})

    def post(self, request):
        user = User.objects.create_user(request.data.get("username"), email=request.data.get("email"), password=request.data.get("password"))
        serializer = NewUserSerializer(user, data=request.data, context = {'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'user': user})
        serializer.save()
        return redirect('user_list')


#deleting self causes forced logout
class DeleteUser(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/delete_user.html'

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        return Response({'user': user})

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return redirect('user_list')


#need to assign template to this view
#changing password causes forced logout
class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
#        renderer_classes = [TemplateHTMLRenderer]
#        template_name = 'user/change_password.html'
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                return Response("Success.", status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
def dashboard(request):
    return render(request, template_name='admin.html')


@login_required 
def list_recipients(request):
    recipients = Refugee.objects.all().values_list('first_name','middle_name','last_name','gender','age','phone_number','demographic_info','ethnicity',
        'city','id')
    recipients_json = json.dumps(list(recipients), cls=DjangoJSONEncoder)
    return render(request, 'refugee/recipient_list.html', context={"recipient": recipients_json})


@login_required 
def edit_recipients(request):
    form = RefugeeForm()
    if request.method.lower() == "post":
        form = RefugeeForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'refugee/edit_recipients.html', context={"form": form})


@login_required 
def recipients_detail(request, recipient_id):
    recipient_obj = get_object_or_404(Refugee, id=recipient_id)
    form = RefugeeForm(instance=recipient_obj)
    if request.method.lower() == "post":
        form = RefugeeForm(request.POST,instance=recipient_obj)
        if form.is_valid():
            form.save()
            return redirect('/admin/view_recipients/')

    return render(request, 'refugee/edit_recipients.html', context={"form": form})


@login_required 
def edit_messages(request):
    form = CallMessageForm()
    if request.method.lower() == "post":
        form = CallMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'message/edit_message.html', context={"form": form})


@login_required 
def list_call_messages(request):
    messages = CallMessage.objects.all().values_list('title', 'category', 'audio', 'duration', 'content','id')
    messages_json = json.dumps(list(messages), cls=DjangoJSONEncoder)
    print(messages_json)
    return render(request, 'message/message_list.html', context={"messages": messages_json})


@login_required 
def call_message_detail(request, call_message_id):
    message_obj = get_object_or_404(CallMessage, pk=call_message_id)
    form = CallMessageForm(instance=message_obj)
    audio_path = CallMessage.objects.values('audio').filter(pk=call_message_id)
    audio_url = settings.url + audio_link[0].get('audio')
    
    return render(request, 'message/edit_message.html', context={"form": form, 'audio': audio_url})


@login_required 
@staff_member_required
def create_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html',context={"form" : form})

@login_required 
@staff_member_required
def user_list(request):
    users = User.objects.all().values_list('username', 'email','first_name','last_name')
    users_json = json.dumps(list(users), cls=DjangoJSONEncoder)
    return render(request, 'registration/userlist.html',context={"users" : users_json})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')

