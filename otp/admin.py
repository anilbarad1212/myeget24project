import imp
from django.contrib import admin
from .models import Code


# Register your models here.
class OtpAddmin(admin.ModelAdmin):
    list_display = ('id', 'otp', 'user', 'date_added')


admin.site.register(Code, OtpAddmin)
