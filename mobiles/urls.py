"""phone_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path
from django.contrib import admin
from mobiles import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .forms import MyPasswordResetForm, MySetPasswordForm
from django.views.static import serve

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name="show-cart"),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removescart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profileView, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('verify/', views.verify_view, name='verify'),
    path('change_number/', views.change_phone_number, name='change_number'),
    path('checkout/', views.checkout, name='checkout'),
    path('all--mobiles/<slug:data>', views.all_mobiles, name='all-mobiles'),
    path('accesories/<int:id>', views.accesories_view, name='all_parts'),
    path('product-detail/<int:id>',
         views.product_detail,
         name='product-detail'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='mobiles/password_reset.html',
             form_class=MyPasswordResetForm),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='mobiles/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='mobiles/password_reset_confirm.html',
             form_class=MySetPasswordForm),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='mobiles/password_reset_complete.html'),
         name='password_reset_complete'),
    path('search/', views.search, name='search-product'),
    path('return/<int:id>', views.return_order, name='return-order'),
    path('cancel-return-request/<int:id>',
         views.cancel_return_request,
         name='cancel-return-request'),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
