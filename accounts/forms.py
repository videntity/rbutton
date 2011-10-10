#!/usr/bin/env python
from django import forms
from b4b.accounts.models import *
#from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.localflavor.us.forms import *
from registration.forms import RegistrationFormUniqueEmail
from registration.models import RegistrationProfile
from models import gender_choices, annon_choices
from utils import create_restcat_user
from django.core.mail import send_mail
from b4b import settings
import pycurl, StringIO

class RegistrationForm(RegistrationFormUniqueEmail):
    username = forms.CharField(max_length=30, label="Username*")
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password*")
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=30, label="Password(again)*")
    email = forms.EmailField(max_length=75, label="Email*")
    first_name = forms.CharField(max_length=30, label="First Name*")
    last_name = forms.CharField(max_length=30, label="Last Name*")
    #email = forms.EmailField(max_length=50, label="WVU MIX Email")
    mobile_phone_number = forms.CharField(max_length=15, required=False,
                            label="Mobile Phone Number")
    annon = forms.TypedChoiceField(widget=forms.RadioSelect, label="Security (Public Reccomended)*", choices=annon_choices)
    pin = forms.CharField(max_length=4,label="4 Digit PIN* (Used for Weight Ins)",widget=forms.PasswordInput)
    gender =forms.TypedChoiceField(widget=forms.RadioSelect, label="Gender*", choices=gender_choices)
    height_in = forms.TypedChoiceField(label="""Height*""", choices=height_choices )
    weight_goal = forms.IntegerField(label="Goal Weight(lbs)*")
    twitter = forms.CharField(max_length=100, required=False,
                            label="Twitter ID")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        if len(password1) < settings.MIN_PASSWORD_LEN:
            msg="Password must be at least %s characters long.  Be tricky!" % (settings.MIN_PASSWORD_LEN)
            raise forms.ValidationError(msg)
        return password2


    #def clean_password(self):
    #    data = self.cleaned_data['password']
    #    if len(data)<8:
    #        raise forms.ValidationError("Your password must be at least 6 characters.")
    #    return data

    def clean_pin(self):
        data = self.cleaned_data['pin']
        if len(data)!=4:
            raise forms.ValidationError("Your PIN must be exactly 4 digits")
        if not str(data).isdigit():
            raise forms.ValidationError("Your PIN must be a number")
        return data
    
    def clean_username(self):
        data = self.cleaned_data['username']
        URL="%sapi/accounts/checkusernameexists/%s/" % (settings.RESTCAT_SERVER, data)
        
        user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
        URL=str(URL)
    
        c = pycurl.Curl()
        c.setopt(pycurl.URL, URL)
        c.setopt(c.SSL_VERIFYPEER, False)
        b = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.HTTPHEADER, ["Accept:"])
        c.setopt(pycurl.USERPWD, user_and_pass)
        c.perform()
        httpcode=c.getinfo(c.HTTP_CODE)
        if httpcode==200:
            raise forms.ValidationError("Sorry this username is already taken.")
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        mix = data.split(settings.RESTRICT_REG_DOMAIN_TO)
        if settings.RESTRICT_REG_DOMAIN_TO:
            if len(mix)==1:
                er="You must have a '%s' email to register." % (settings.RESTRICT_REG_DOMAIN_TO)
                raise forms.ValidationError(er)
        
        URL="%sapi/accounts/checkexists/%s/" % (settings.RESTCAT_SERVER, data)
        
        user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
        URL=str(URL)
    
        c = pycurl.Curl()
        c.setopt(pycurl.URL, URL)
        c.setopt(c.SSL_VERIFYPEER, False)
        b = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.HTTPHEADER, ["Accept:"])
        c.setopt(pycurl.USERPWD, user_and_pass)
        c.perform()
        httpcode=c.getinfo(c.HTTP_CODE)
        if httpcode==200:
            raise forms.ValidationError("Sorry this email address is already registered.")
        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data
    
    def clean_mobile_phone_number(self):
        data = self.cleaned_data['mobile_phone_number']
        newdata=""
        l=['0','1','2','3','4','5','6','7','8','9']
        for i in data:
            if i in l:
                newdata+=i
        data=newdata
        URL="%sapi/accounts/checkmobileexists/%s/" % (settings.RESTCAT_SERVER, data)
        
        user_and_pass="%s:%s" % (settings.RESTCAT_USER, settings.RESTCAT_PASS)
        URL=str(URL)
    
        c = pycurl.Curl()
        c.setopt(pycurl.URL, URL)
        c.setopt(c.SSL_VERIFYPEER, False)
        b = StringIO.StringIO()
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)
        c.setopt(pycurl.HTTPHEADER, ["Accept:"])
        c.setopt(pycurl.USERPWD, user_and_pass)
        c.perform()
        httpcode=c.getinfo(c.HTTP_CODE)
        if httpcode==200:
            raise forms.ValidationError("Sorry this mobile phone number is already registered.")
        
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

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
            annon=self.cleaned_data.get('annon', ""),
            height_in=self.cleaned_data.get('height_in', ""),
            pin=self.cleaned_data.get('pin', ""),
            gender=self.cleaned_data.get('gender', ""),
            mobile_phone_number=self.cleaned_data.get('mobile_phone_number', ""),
            twitter=self.cleaned_data.get('twitter', ""),
            weight_goal=self.cleaned_data.get('weight_goal', ""),
            )
        r=create_restcat_user(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password1'],
                            first_name= self.cleaned_data.get('first_name', ""),
                            last_name= self.cleaned_data.get('last_name', ""),
                            email=self.cleaned_data['email'],
                            height_in=self.cleaned_data.get('height_in', ""),
                            weight_goal=self.cleaned_data.get('weight_goal', ""),
                            gender=self.cleaned_data.get('gender', ""),
                            pin=self.cleaned_data.get('pin', ""),
                            birthdate="2010-01-01",
                            mobile_phone_number=self.cleaned_data.get('mobile_phone_number', ""),
                            twitter=self.cleaned_data.get('twitter', ""),
                            )
        if r['code']!="200":
            
            """Return an email telling the user."""
            body="%s\n%s" % (r['message'], "Please contact the system administator with this error. Your RESTCat account was not created.")
            #print body
            send_mail('We encountered a problem when creating your account.', body, 'help@videntity.com',
                    [new_user.email], fail_silently=False)
            new_user.delete()
            return None
        else:
            return new_user

class AccountSettingsForm(forms.Form):
    annon = forms.TypedChoiceField(widget=forms.RadioSelect, label="Anonymous*", choices=annon_choices)
    height_in = forms.TypedChoiceField(choices=height_choices, label="Height*")
    weight_goal = forms.IntegerField(label="Goal Weight(lbs)*")
    gender =forms.TypedChoiceField(widget=forms.RadioSelect, label="Gender*", choices=gender_choices)
    twitter = forms.CharField(max_length=100, required=False, label="Twitter ID")
    
