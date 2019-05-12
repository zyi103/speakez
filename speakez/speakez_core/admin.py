from django.contrib import admin
from .models import Refugee, Category, CallMessage

# Register your models here.
admin.site.register(Refugee)
admin.site.register(Category)
admin.site.register(CallMessage)

