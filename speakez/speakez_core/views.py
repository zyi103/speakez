from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import parser_classes, action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
class ViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @method_decorator(login_required(login_url='/accounts/login/'))
    @action(detail=False, methods=['get'])
    def admin(self, request):
        return render(request, template_name='admin.html')

