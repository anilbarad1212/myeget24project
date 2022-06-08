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


class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'address1', 'address2', 'landmark',
                    'city', 'state', 'pincode', 'mobile_number', 'date_added')


class AllBrandsAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand_name', 'brand_photo', 'date_added')


class AllMobilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'all_brands', 'mobile_name', 'release_date',
                    'display_size', 'mobile_photo', 'date_added')


class AllAccesoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'all_mobiles', 'title', 'price', 'description',
                    'category', 'sub_category', 'color', 'availability',
                    'accesories_photo', 'date_added')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'all_accesories', 'quantity', 'date_added')


class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'payment_status', 'user',
                    'customer_address', 'all_accesories', 'quantity',
                    'item_total_price', 'expected_delivery_date', 'message',
                    'status', 'ordered_date', 'updated_at')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order_number', 'user', 'email',
                    'total_price')


admin.site.register(CustomerAddress, CustomerAddressAdmin)
admin.site.register(All_Brands, AllBrandsAdmin)
admin.site.register(All_Mobiles, AllMobilesAdmin)
admin.site.register(All_Accesories, AllAccesoriesAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderPlaced, OrderPlacedAdmin)
admin.site.register(Payment, PaymentAdmin)
