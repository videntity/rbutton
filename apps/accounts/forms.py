#!/usr/bin/env python
from django import forms
from  models import *
#from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.contrib.localflavor.us.forms import *
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile
from django.conf import settings

from django import forms

class SocialProfileForm(forms.Form):
    first_name = forms.CharField(max_length = 30, label = 'First Name')
    last_name = forms.CharField(max_length = 30, label = 'Last Name')
    #(Optional) Make email unique.
    email = forms.EmailField(label = 'Email Address')


# ==================
class UserCreationFormExtended(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = True
        self.fields['email'].label = 'email*:'
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
# ==================


class UserProfileDisplay(ModelForm):
    first_name              = forms.CharField(required=False, max_length=30)
    last_name               = forms.CharField(required=False, max_length=40)
    email                   = forms.CharField(required=False, max_length=75)

    class Meta:
        model = UserProfile
        exclude = ('user', 'security_level','user_type','approval_status')


        def save(self, ):
            nup = UserProfile.objects.create(
                username=User,
                first_name=self.cleaned_data['first_name'],last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email_address'],
            )

            return username




class PasswordResetRequestForm(forms.Form):
    email= forms.CharField(max_length=75, label="Email")

class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password*")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password (again)*")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg="Password must be at least %s characters long.  Be tricky!" % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password")
    smscode  = forms.CharField(widget=forms.PasswordInput, max_length=5, label="SMS Code")


class SimpleLoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password")


class SMSCodeForm(forms.Form):
    username= forms.CharField(max_length=30, label="Username")



class RegistrationForm(RegistrationFormUniqueEmail):
    username = forms.CharField(max_length=30, label="Username*")
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password*")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password (again)*")
    email = forms.EmailField(max_length=75, label="Email*")
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=60, label="Last Name")
    phone_number = forms.CharField(max_length=15, label="Phone Number")
    twitter = forms.CharField(max_length=15, label="Twitter")
    organization_name = forms.CharField(max_length=100, label="Organization Name*")
    

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg="Password must be at least %s characters long.  Be tricky!" % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2


    def save(self, profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(
                        username=self.cleaned_data['username'],
                        password=self.cleaned_data['password1'],
                        email=self.cleaned_data['email'],
                        profile_callback=profile_callback)
        new_user.first_name = self.cleaned_data.get('first_name', "")
        new_user.last_name = self.cleaned_data.get('last_name', "")
        new_user.save()
        UserProfile.objects.create(
            user=new_user,
            mobile_phone_number=self.cleaned_data.get('mobile_phone_number', ""),
            )
        
        return new_user

class AccountSettingsForm(forms.Form):
    first_name      = forms.CharField(max_length=30, required=False, label="First Name")
    last_name       = forms.CharField(max_length=60, required=False, label="Last Name")
    phone_number    = forms.CharField(max_length=15, required=False, label="Phone Number")
    email           = forms.EmailField(max_length=75, required=True, label="Email*")
    twitter         = forms.CharField(max_length=15, required=False, label="Twitter")

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length = 30, label = 'First Name')
    last_name = forms.CharField(max_length = 30, label = 'Last Name')
    #(Optional) Make email unique.
    email = forms.EmailField(label = 'Email Address')
    

