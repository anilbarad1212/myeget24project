from pyexpat import model
from django.contrib import admin
from requests import request
from .models import *
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
import datetime
from .utils import sent_dileverd_message


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
                    'display_size', 'mobile_photo', 'date_added', 'click_me')

    def click_me(self, obj):
        return format_html(
            f'<a href="/admin/mobiles/all_mobiles/{obj.id}/change/" class="default" >View</a>'
        )


class AllAccesoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'all_mobiles', 'title', 'price', 'description',
                    'category', 'sub_category', 'color', 'availability',
                    'accesories_photo', 'date_added')


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'all_accesories', 'quantity', 'date_added')


class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_number',
        'payment_status',
        'user',
        'customer_address',
        'all_accesories',
        'quantity',
        'item_total_price',
        'expected_delivery_date',
        'message',
        'status',
        'ordered_date',
        'updated_at',
    )
    actions = ('order_dilevered', )

    def order_dilevered(self, request, queryset):
        for i in queryset:
            user = i.user
            phone_number = i.user.phone_number
            product = i.all_accesories.title
            quantity = i.quantity
            total_price = i.item_total_price
            tday = datetime.date.today()
            month = tday.strftime("%B")
            years = tday.strftime("%Y")
            weekday = tday.strftime("%A")
            date = tday.strftime("%d")
            delivery_date = weekday + ' ' + date + ' ' + month + ' ' + years
            sent_dileverd_message(user, phone_number, product, quantity,
                                  total_price, delivery_date)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'order_number_color', 'user', 'email',
                    'total_price', 'view_data')
    actions = ('dilevered', )

    def order_number_color(self, obj):
        return format_html(
            f'<span style="color:red">{obj.order_number}</span>')

    def view_data(self, obj):
        return format_html(
            f'<a href="/admin/mobiles/payment/{obj.payment_id}/change/" class="default" style="color:red" >View</a>'
        )


class ReturnOrdertAdmin(admin.ModelAdmin):
    list_display = ('order_placed', 'return_request', 'return_status',
                    'return_request_date')


admin.site.register(CustomerAddress, CustomerAddressAdmin)
admin.site.register(All_Brands, AllBrandsAdmin)
admin.site.register(All_Mobiles, AllMobilesAdmin)
admin.site.register(All_Accesories, AllAccesoriesAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(OrderPlaced, OrderPlacedAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Return_Order, ReturnOrdertAdmin)
