from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Refugee, Category, CallMessage
from django.contrib.auth.models import User
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated   
from .serializers import UserSerializer, ChangePasswordSerializer
from .forms import CallMessageForm
from django.views.generic.edit import FormView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView


class UserList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_list.html'

    def get(self, request):
        queryset = User.objects.all().order_by('-date_joined')
        return Response({'users': queryset})


class UserDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'refugees/user_detail.html'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response({'serializer': serializer, 'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'user': user})
        serializer.save()
        return redirect('user-list')


class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
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

#need to add to admin.html and urls
class CallMessageView(FormView):
    template_name = 'refugee/record_message.html'
    form_class = CallMessageForm
    success_url = '/record_message/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
