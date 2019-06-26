from django.http import HttpResponse
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Refugee, Category, CallMessage, CallLog, CallLogDetail, CallStatus
from .forms import CallMessageForm, RefugeeForm, CategoryForm, CallStatusForm
from django.core.cache import cache
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
import logging
import uuid
from itertools import chain


   

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
    print()
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
        account_sid = settings.TWILIO_KEY
        auth_token = settings.TWILIO_TOKEN
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
        audio_path = CallMessage.objects.filter(pk=call_message_id).first().audio.path
        cache_key = uuid.uuid4().hex
        cache.set(cache_key, audio_path , 300)
        cache_url = '{}://{}'.format(request.scheme, request.get_host()) + '/audio_message/' + cache_key + '/'
      

        # -----------------------------------------------------------
        # DEVELOPMENT 
        # audio_url = 'https://ccrma.stanford.edu/~jos/wav/gtr-nylon22.wav'  
        #################################################################
        xml_string = '<Response><Play>' + cache_url + '</Play></Response>'
        twimlet_url = urllib.parse.quote_plus(xml_string)


        # getting phone number 
        recipients_id = request.POST.getlist('recipients[]')
        print(recipients_id)
        recipients = list(Refugee.objects.filter(pk__in=recipients_id).values())

        
        # calling maximum recipient limit
        if len(recipients) < 5:
            sid_list = []
            for i in range(len(recipients)):
                # xml url created by echo Twimlet
                url = 'https://twimlets.com/echo?Twiml=' + twimlet_url
                phone_num = '+1' + recipients[i].get('phone_number')
                host_num = settings.TWILIO_PHONE_NUM
                callback_url = '{}://{}'.format(request.scheme, request.get_host()) + '/twilio/call_status_event/'

                call = client.calls.create(
                                    machine_detection='Enable',
                                    status_callback= callback_url,
                                    status_callback_method='POST',
                                    url= url,
                                    to= phone_num,
                                    from_= host_num
                                )

                #logging
                clog_detail = CallLogDetail(recipient=Refugee(**recipients[i]),call_log=clog, call_sid=call.sid)
                clog_detail.save()
                # sid_list.append(call.sid)
                # print("[%s] is called by [%s] with [%s] at [%s]" % (clog_detail.recipient.first_name,
                #                                                     clog_detail.call_log.admin_username,
                #                                                     clog_detail.call_log.message_sent, 
                #                                                     clog_detail.call_log.date_time_created))
        else:
            return HttpResponse("Too many recipients", status=400)
                
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
    category = Category.objects.all()
    if request.method.lower() == "post":
        form = CallMessageForm(request.POST, request.FILES)
        print('==========================================')
        print(form)
        if form.is_valid():
            print("valid")
            form.save()
    return render(request, 'message/edit_message.html', context={"form": form, 'category': category, 'is_update': False})

@login_required 
def add_category(request):
    form = CategoryForm()
    if request.method.lower() == "post":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_message')
    return render(request, 'message/add_category.html', context={"form": form})


@login_required 
def list_call_messages(request):
    messages_list = CallMessage.objects.all()
    messages = create_messages_json(messages_list)
    print(messages)
    return render(request, 'message/message_list.html', context={"messages": messages})

def create_messages_json(messages_list):
    messages = []
    for message in messages_list:
        message_dict = {}
        message_dict['title'] = message.title
        message_dict['category'] = str(message.category.title)
        message_dict['audio_name'] = message.audio.name
        message_dict['duration'] = message.duration
        message_dict['content'] = message.content
        message_dict['id'] = message.id
        print(message_dict)
        messages.append(message_dict)
    return json.dumps(list(messages), cls=DjangoJSONEncoder)
    


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
@csrf_exempt
def view_report(request):
    reports = []

    if request.user.is_superuser:
        call_list = CallLog.objects.all().values()
    else:
        user_id = request.user.id
        call_list = CallLog.objects.filter(admin_id=user_id).values()
    calls = [entry for entry in call_list]
    for call in calls:
        call_log_id = call['id']
        call_time = call['date_time_created']
        call_message = get_call_message(call['message_sent_id'])
        audio_name = call_message.audio.name
        category = call_message.category
        content = call_message.content
        call_event_count = get_call_count(call_log_id)
        success_event_count = get_success_count(call_log_id)
        recipient_list = get_recipient_list(call_log_id)
        message_id = CallLog.objects.filter(pk=call_log_id).first().message_sent_id

        report = create_report(call_log_id,call_time,category,content,audio_name,call_event_count,success_event_count,recipient_list,message_id)
        reports.append(report)
    
    return render(request, 'report/view_report.html', context={'calls': reports})

def get_success_count(call_log_id):
    # Twilio call
    account_sid = settings.TWILIO_KEY
    auth_token = settings.TWILIO_TOKEN
    client = Client(account_sid, auth_token)

    success_count = 0
    call_log_details = CallLogDetail.objects.filter(call_log_id=call_log_id)
    if (len(call_log_details) > 0):
        for call_event in call_log_details:
            call_status = client.calls(call_event.call_sid).fetch().status
            if (call_status == "completed"):
                success_count += 1
    return success_count

def get_call_count(call_log_id):
    call_log_details = CallLogDetail.objects.filter(call_log_id=call_log_id)
    return len(call_log_details)

def get_recipient_list(call_log_id):
    recipient_list = []
    call_log_details = CallLogDetail.objects.filter(call_log_id=call_log_id).values()
    for call_event in call_log_details:
        recipient_list.append(str(call_event['recipient_id']))
    return recipient_list

def create_report(call_log_id, datetime, category, content, audio_name, call_event_count, success_event_count, recipient_list, message_id):
    report = {}
    report['call_log_id'] = str(call_log_id)
    report['date'] = datetime.strftime("%m/%d/%Y")
    report['time'] = datetime.strftime("%H:%M:%S")
    report['category'] = str(category)
    report['content'] = content
    report['audio_name'] = audio_name
    report['call_event_count'] = call_event_count
    report['success_event_count'] = success_event_count
    report['recipient_list'] = recipient_list
    report['message_id'] = str(message_id)
    return report

def get_call_message(message_sent_id):
    call_message = CallMessage.objects.filter(pk=message_sent_id).first()
    return call_message

@login_required
def view_report_detail(request, call_log_id):
    # Twilio call
    account_sid = settings.TWILIO_KEY
    auth_token = settings.TWILIO_TOKEN
    client = Client(account_sid, auth_token)

    message_id = CallLog.objects.filter(pk=call_log_id).first().message_sent_id
    message = CallMessage.objects.filter(pk=message_id).first()

    recipients = []
    call_details = list(CallLogDetail.objects.filter(call_log_id=call_log_id).values())
    for i in range(len(call_details)):
        recipient = Refugee.objects.filter(pk=call_details[i]['recipient_id']).values().first()
        twilio_report = client.calls(call_details[i]['call_sid']).fetch()
        recipients.append(create_report_detail(recipient, twilio_report))
    recipients = json.dumps(recipients)
    return render(request, 'report/view_report_detail.html', context={"message" : message, "recipients": recipients})

def create_report_detail (recipient, twilio):
    report_detail = {}
    report_detail['id'] = str(recipient['id'])
    report_detail['first_name'] = recipient['first_name']
    report_detail['middle_name'] = recipient['middle_name']
    report_detail['last_name'] = recipient['last_name']
    report_detail['phone_number'] = recipient['phone_number']
    
    report_detail['duration'] = twilio.duration
    report_detail['status'] = twilio.status
    return report_detail

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

@login_required
def get_audio_file(request, filename):
    filename = os.path.join(settings.BASE_DIR,'media',filename)
    return FileResponse(open(filename, 'rb'))

def get_audio_message(request, key):
    audio_path = cache.get(key)
    if audio_path is not None:
        return FileResponse(open(audio_path, 'rb'))
    else:
        return HttpResponse('audio not get, key: ' + key,status=550)


@csrf_exempt
def save_call_status(request):
    if request.method.lower() == 'post':
        logger = logging.getLogger('django')
        call_status = json.dumps(dict(request.POST))
        logger.info('======================call_status==================')
        logger.info(call_status)
        logger.info(type(call_status))

        form = CallStatusForm(call_status)
        if form.is_valid:
            logger.debug('======================START SAVING==================')
            form.save()
            logger.debug("saved!!!")
            return HttpResponse('callback recieved,' + str(call_status) ,status=200)
        else: 
            return HttpResponse('form not valid' ,status=560)



def view_callback(request):
    return FileResponse(open(os.path.join(settings.BASE_DIR,'speakez_core','debug.log'),'rb'),status=200)