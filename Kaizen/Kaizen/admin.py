from django.contrib import admin 
from .models import *
from django.db.models import Sum
  
admin.site.register(BMR)
admin.site.register(Profile)
admin.site.register(RunningMacro)
