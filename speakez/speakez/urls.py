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
from django.conf.urls import url, include
from speakez_core import views
from django.views.generic import RedirectView
from django.urls import include, path
from rest_framework import routers
from speakez_core import views

urlpatterns = [
    path('admin/view_users/', views.UserList.as_view(), name='user_list'),
    path('admin/view_users/new_user/', views.NewUser.as_view(), name='new_user'),
    path('admin/view_users/change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('admin/view_users/<str:username>/', views.UserDetail.as_view(), name='user_detail'),
    path('admin/view_users/<str:username>/delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/create_user/', views.create_user),
    path('accounts/users/', views.user_list),
    path('accounts/users/<str:username>/', views.UserDetail.as_view(), name='user_detail'),
    path('admin/', views.dashboard),
    path('admin/recipients/', views.list_recipients),
    path('admin/edit_recipients/', views.edit_recipients),
    path('admin/edit_messages/', views.edit_messages),
    path('admin/view_messages/', views.list_call_messages),
    path('admin/view_messages/<int:call_message_id>/', views.call_message_detail, name='call_message_detail'),
    url(r'^', RedirectView.as_view(url='/accounts/login/'))
]
