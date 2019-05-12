"""speakez URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url, include
from speakez_core import views
from django.views.generic import RedirectView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', views.dashboard),
    path('admin/recipients', views.list_recipients),
<<<<<<< HEAD
    path('admin/messages', views.edit_messages),
    path('admin/view_messages', views.list_call_messages),
    path('admin/view_messages/<int:call_message_id>/', views.call_message_detail, name='call_message_detail'),
=======
    path('admin/view_messages', views.list_call_messages),
    path('admin/view_messages/<int:call_message_id>/', views.call_message_detail, name='call_message_detail'),
    path('admin/messages', views.list_messages),
>>>>>>> staging
    url(r'^', RedirectView.as_view(url='/accounts/login/'))
]
