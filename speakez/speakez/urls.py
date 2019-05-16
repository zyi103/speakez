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
from speakez_core import views
from django.views.generic import RedirectView
from django.urls import include, path
from rest_framework import routers
from speakez_core import views
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create_user/', views.create_user, name='new_user'),
    path('accounts/users/', views.user_list, name='user_list'),
    path('accounts/users/<str:username>/', views.UserDetail.as_view(), name='user_detail'),
    path('admin/view_users/<str:username>/delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    path('admin/', views.dashboard, name='dashboard'),
    path('admin/edit_recipients/', views.edit_recipients, name='edit_recipient'),
    path('admin/edit_recipients/<str:recipient_id>/', views.recipients_detail, name='recipient_detail'),
    path('admin/view_recipients/', views.list_recipients, name='recipient_list'),
    path('admin/edit_messages/', views.edit_messages),
    path('admin/edit_messages/<str:call_message_id>/', views.call_message_detail, name='call_message_detail'),
    path('admin/view_messages/', views.list_call_messages, name='message_list'),
    url(r'^', RedirectView.as_view(url='/accounts/login/'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
