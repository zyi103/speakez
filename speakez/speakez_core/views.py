from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Refugee, Category, CallMessage
from django.contrib.auth.models import User
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


@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, template_name='admin.html')


def list_recipients(request):
    recipients = Refugee.objects.all()
    return render(request, 'refugee/list.html', context={"refugees": recipients})
    

def list_call_messages(request):
    ordered_call_messages = CallMessage.objects.order_by('-date_time_created')
    return render(request, 'refugee/messages.html', context={"messages": ordered_call_messages})


def call_message_detail(request, call_message_id):
    call_message = get_object_or_404(CallMessage, pk=call_message_id)
    return render(request, 'refugee/message_detail.html', context={"message": call_message})

