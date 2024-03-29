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
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(r'', RedirectView.as_view(url='/accounts/login/'), name='admin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create_user/', views.create_user, name='new_user'),
    path('accounts/users/', views.user_list, name='user_list'),
    path('accounts/users/<str:username>/', views.UserDetail.as_view(), name='user_detail'),
    path('admin/view_users/<str:username>/delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    path('admin/', views.dashboard, name='dashboard'),
    path('admin/edit_recipients/', views.edit_recipients, name='edit_recipient'),
    path('admin/edit_recipients/<uuid:recipient_id>/', views.recipients_detail, name='recipient_detail'),
    path('admin/view_recipients/', views.list_recipients, name='recipient_list'),
    path('admin/select_recipients/', views.select_recipients, name='select_recipients'),
    path('admin/delete_recipients/', views.delete_recipient, name='delete_recipient'),
    path('admin/select_recipients/select_message/<recipients>/', views.select_message, name='select_message'),
    path('admin/call_recipients/', views.call_recipients, name='call_recipients'),
    path('admin/view_report/', views.view_report, name='view_report'),
    path('admin/view_report/<uuid:call_log_id>/', views.view_report_detail, name='view_report_detail'),
    path('admin/add_messages/', views.add_message, name='add_message'),
    path('admin/add_category/', views.add_category, name='add_category'),
    path('admin/view_messages/<uuid:call_message_id>/', views.call_message_detail, name='update_message_detail'),
    path('admin/delete_messages/', views.delete_message, name='delete_message'),
    path('admin/view_messages/', views.list_call_messages, name='message_list'),
    path('admin/audio/<path:filename>/', views.get_audio_file, name='get_audio_file'),
    path('audio_message/<key>/', views.get_audio_message, name='get_audio_message'),
    path('twilio/call_status_event/', views.save_call_status, name='save_call_status'),
    path('twilio/debug/', views.view_callback),
    # url(r'^', RedirectView.as_view(url='/accounts/login/'))
    # this redirect will not allow websever to serve message from media file.
    # use 404 redirect page instead
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
