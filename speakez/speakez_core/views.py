from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Refugee, Category, CallMessage, CallLog, CallLogDetail
from .forms import CallMessageForm, RefugeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated   

from twilio.rest import Client
from twilio.twiml.voice_response import Play, VoiceResponse

from speakez_core.forms import SignUpForm

from .serializers import UserSerializer, NewUserSerializer, ChangePasswordSerializer
from .forms import CallMessageForm
from django.views.generic.edit import FormView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

import os, os.path, time
import datetime
import unicodedata
import json
import urllib
   

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
@csrf_exempt
def select_recipients(request):
    recipients_json = serializers.serialize('json', Refugee.objects.all())
    # redirect the select recipients list through view for validation
    # if request.method.lower() == "post":
    #     recipients_list = request.POST.getlist('data[]')
    #     if recipients_list != '':
    #         recipients_url = '&'.join((x) for x in recipients_list)
    #         print(redirect('select_message', recipients=recipients_url))
    #         return redirect('select_message', recipients=recipients_url)
    return render(request, 'refugee/select_recipients.html', context={"recipient": recipients_json})


@login_required 
def select_message(request, recipients):
    messages_json = serializers.serialize('json', CallMessage.objects.all())
    recipients = recipients.split('&')
    return render(request, 'refugee/select_message.html', context={"recipients": recipients, "messages": messages_json})


@login_required 
@csrf_exempt
def call_recipients(request):
    if request.method.lower() == "post":
        
        # Twilio call
        account_sid = 'AC8bbf41596517948ed9b6ad40ac16ff45'
        auth_token = '34437a52ec6179fef5b40dc49b7303bb'
        client = Client(account_sid, auth_token)

        # logging
        call_message_id = request.POST.getlist('message[pk]')[0]
        message_instance = CallMessage.objects.filter(pk=call_message_id).first()
        clog = CallLog(admin_id=request.user.id, admin_username=request.user.username, message_sent=message_instance)
        clog.save()

        #################################################################
        # getting audio
        # replace audio_url to the wav file in production env
        # comment this line out in production env to recieve the actual call message
        # ===============================================================
        # PRODUCTION
        # audio_url = request.POST.getlist('message[audio_url]')[0]
        # -----------------------------------------------------------
        # DEVELOPMENT 
        audio_url = 'https://ccrma.stanford.edu/~jos/wav/gtr-nylon22.wav'  
        #################################################################
        xml_string = '<Response><Play>' + audio_url + '</Play></Response>'
        twimlet_url = urllib.parse.quote_plus(xml_string)


        # getting phone number 
        recipients_id = request.POST.getlist('recipients[]')
        recipients = list(Refugee.objects.filter(pk__in=recipients_id).values())

        # 
        sid_list = []
        for i in range(len(recipients)):
            # calling maximum recipient limit
            if i < 5:
                # xml url created by echo Twimlet
                url = 'https://twimlets.com/echo?Twiml=' + twimlet_url
                phone_num = '+1' + recipients[i].get('phone_number')
                call = client.calls.create(
                                    url= url,
                                    to= phone_num,
                                    from_='+16414549805'
                                )

                #logging
                clog_detail = CallLogDetail(recipient=Refugee(**recipients[i]),call_log=clog, call_sid=call.sid)
                clog_detail.save()
                sid_list.append(call.sid)
                print("[%s] is called by [%s] with [%s] at [%s]" % (clog_detail.recipient.first_name,
                                                                    clog_detail.call_log.admin_username,
                                                                    clog_detail.call_log.message_sent, 
                                                                    clog_detail.call_log.date_time_created))
            else:
                return HttpResponse(status=201)

        calls = client.calls.list(limit=100)
        for record in calls:
            print(record.sid)
            print(record.status)

        return HttpResponse(status=200)


@login_required 
def edit_recipients(request):
    form = RefugeeForm()
    if request.method.lower() == "post":
        form = RefugeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipient_list')
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
def add_message(request):
    form = CallMessageForm()
    if request.method.lower() == "post":
        form = CallMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, 'message/edit_message.html', context={"form": form, 'is_update': False})


@login_required 
def list_call_messages(request):
    messages = CallMessage.objects.all().values_list('title', 'category', 'audio', 'duration', 'content','id')
    messages_json = json.dumps(list(messages), cls=DjangoJSONEncoder)
    print(messages_json)
    return render(request, 'message/message_list.html', context={"messages": messages_json})


@login_required 
def call_message_detail(request, call_message_id):
    message = CallMessage.objects.get(pk=call_message_id)
    form = CallMessageForm(instance=message)
    if request.method.lower() == "post":
        form = CallMessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            file_path = settings.MEDIA_ROOT + '/uploads/' + message.title + '.wav'
            print(file_path + '_OLD')
            os.replace(file_path,  file_path + '_OLD')
            # os.remove(file_path)
            form.save()
            
    
    return render(request, 'message/edit_message.html', context={"form": form, 'is_update': True, 'message': message})

@login_required 
def view_report(request):
    user = request.user.username
    
    
    return render(request, 'report/view_report.html')


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


