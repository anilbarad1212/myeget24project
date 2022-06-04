from pyexpat import model
from django.contrib import admin
from .models import *
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (*UserAdmin.fieldsets, ('contact info', {
        'fields': ('phone_number', )
    }))


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomerAddress, )
admin.site.register(All_Brands, )
admin.site.register(All_Mobiles, )
admin.site.register(All_Accesories, )
admin.site.register(Cart, )
admin.site.register(OrderPlaced, )
admin.site.register(Payment, )
