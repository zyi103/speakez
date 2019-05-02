from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import parser_classes, action

class ViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        return render(request, template_name='dashboard.html')

