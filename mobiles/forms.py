from pyexpat import model
from unittest.util import _MAX_LENGTH
from django import forms
from otp.models import Code
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from .models import CustomUser, CustomerAddress
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = "__all__"


class CodeForm(forms.ModelForm):
    number = forms.CharField(label='OTP', help_text='Enter Your OTP Here..')

    class Meta:
        model = Code
        fields = ('number', )


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        label='Confirm Password(again)',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=_("Email"),
                             max_length=254,
                             widget=forms.EmailInput(attrs={
                                 'autocomplete': 'email',
                                 'class': 'form-control'
                             }))
    phone_number = forms.CharField(
        label='Phone-Number',
        max_length=10,
        widget=forms.NumberInput(attrs={
            'autocomplete': 'number',
            'class': 'form-control'
        }))

    class Meta:
        model = CustomUser
        fields = [
            'username', 'password1', 'password2', 'email', 'phone_number'
        ]
        labels = {}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }


class CodeForm(forms.ModelForm):
    number = forms.CharField(label=_('OTP'),
                             help_text='Enter Your OTP Here..',
                             strip=False,
                             widget=forms.NumberInput(attrs={
                                 'autofocus': True,
                                 'class': 'form-control'
                             }))

    class Meta:
        model = Code
        fields = ('number', )


class Change_Mobile_Number_Form(forms.ModelForm):
    phone_number = forms.CharField(label=_('Change-Phone-Number'),
                                   help_text='Enter Number Here',
                                   strip=False,
                                   widget=forms.NumberInput(
                                       attrs={
                                           'autofocus': True,
                                           'autocomplete': False,
                                           'class': 'form-control',
                                           'id': 'chng-num'
                                       }))

    class Meta:
        model = CustomUser
        fields = ('phone_number', )


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class': 'form-control'
    }))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control'
        }))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'place_holder': 'Enter Registered Email Address'
            }))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        }),
        help_text=password_validation.password_validators_help_text_html())

    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        }))
