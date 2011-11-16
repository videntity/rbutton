#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
# accounts.views.py
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from django.db.models import Sum
from django.template import RequestContext, Template, Context
from django.shortcuts import render_to_response
from datetime import datetime
from models import *
from forms import *
from emails import send_reply_email
from utils import verify
from rbutton.apps.accounts.models import UserProfile

# from registration.models import RegistrationProfile


def mylogout(request):
    logout(request)
    return render_to_response('accounts/logout.html',
                              context_instance = RequestContext(request))

    
def simple_login(request):
    form = SimpleLoginForm(request.POST)
    if request.method == 'POST':
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']    
            user=authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                   return HttpResponse("Inactive Account")
            else:
                return HttpResponse("Invalid Username or Password")
            return HttpResponse("Authenticate, send SMS, & redirect to SMSCode")
        else:
         return render_to_response('accounts/login.html',
                              RequestContext(request, {'form': form}))
    return render_to_response('accounts/login.html',
                              context_instance = RequestContext(request,{'form': form,
                                                                 'page_heading': 'Login',
                                                                 'editmode': True,
                                                                 },))
         


def signup(request):
    if request.method == 'POST':
       print "in the POST"
       form = UserCreationFormExtended(request.POST)
       print form
       if form.is_valid():
          print "here we go - in the POST and Valid"
          form.first_name = form.cleaned_data['first_name']
          form.last_name = form.cleaned_data['last_name']
          form.email = form.cleaned_data['email']
          form.save()
          return HttpResponseRedirect(reverse('home'))
    else:
       # in the get
       print "In the GET"
       form = UserCreationFormExtended()
       form.username = 'Username'
       form.email = 'sample.name@example.com'
       form.first_name = 'firstname'
       form.last_name = 'lastname'
       form = UserCreationFormExtended(request.POST)
       return render_to_response('accounts/signup.html',
                                 RequestContext(request, {'form': form,
                                                          'page_heading':'Create Your Account',
                                                          'editmode': True,
                                                }),
                                )

    return render_to_response('accounts/account_settings.html',
                              context_instance = RequestContext(request,
                                                                {'form': form,
                                                                 'page_heading': 'Edit Your Profile',
                                                                 'editmode': True,
                                                                 },)
                              ,)


def reset_password(request, reset_password_key=None):
    try:
        vprk=ValidPasswordResetKey.objects.get(
                                        reset_password_key=reset_password_key)
        
    except:
        return render_to_response('accounts/invalid-key.html',
                              RequestContext(request,
                                             {}))
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            vprk.user.set_password(form.cleaned_data['password1'])
            vprk.user.save()
            vprk.delete()
            logout(request)
            return render_to_response('accounts/reset-password-success.html',
                              RequestContext(request,{}))
        else:
         return render_to_response('accounts/reset-password.html',
                        RequestContext(request, {'form': form,
                            'reset_password_key': reset_password_key}))  
        
    return render_to_response('accounts/reset-password.html',
                              RequestContext(request,
                                    {'form': PasswordResetForm(),
                                    'reset_password_key': reset_password_key}))
        






def password_reset_request(request):
    if request.method == 'POST':

        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():  
            data = form.cleaned_data
            return render_to_response('accounts/password-reset-request.html',
                              RequestContext(request,
                                             {'form': form,
                                              }))
    else:
        return render_to_response('accounts/password-reset-request.html', 
                             {'form': PasswordResetRequestForm()},
                              context_instance = RequestContext(request))
    


def validate_sms(username, smscode):
    try:
        u=User.objects.get(username=username)
        vc=ValidSMSCode.objects.get(user=u, sms_code=smscode)
        now=datetime.now()
    
        if vc.expires < now:
            vc.delete()
            return False
    except(User.DoesNotExist):
        return False        
    except(ValidSMSCode.DoesNotExist):
        return False  
    vc.delete()
    return True


def sms_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print "Authenticate"
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            smscode  = form.cleaned_data['smscode']
            if not validate_sms(username=username, smscode=smscode):
                return HttpResponse("Invalid Access Code")
            
            user=authenticate(username=username, password=password)
            
            if user is not None:

                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                   return HttpResponse("Inactive Account")
            else:
                return HttpResponse("Invalid Username or Password")
            return HttpResponse("Authenticate, send SMS, & redirect to SMSCode")
        else:
         return render_to_response('accounts/login.html',
                              RequestContext(request, {'form': form}))
    return render_to_response('accounts/login.html',
                              context_instance = RequestContext(request)) 

def sms_code(request):
    if request.method == 'POST':
        form = SMSCodeForm(request.POST)
        if form.is_valid():
            try:
                u=User.objects.get(username=form.cleaned_data['username'])
                up=u.get_profile()
                ValidSMSCode.objects.create(user=u)
            except(User.DoesNotExist):
                return HttpResponse("You are not recognized.", status=401)
            except(UserProfile.DoesNotExist):
                return HttpResponse("You do not have a user profile.", status=401)
            
            return HttpResponseRedirect(reverse('login'))
        else:
         return render_to_response('accounts/smscode.html',
                              RequestContext(request, {'form': form}))
    return render_to_response('accounts/smscode.html',
                              context_instance = RequestContext(request)) 

@login_required
def account_settings(request):
    user_id = request.user.id
    user = User.objects.get(pk = user_id)
    user.userprofile = get_or_create_profile(user)
    print user
    print user.userprofile
    form = request.user.get_profile()
    old_email = request.user.email
    print old_email
    form = UserProfileDisplay(request.POST, initial={'username': request.user,
                                       'first_name': request.user.first_name,
                                       'last_name': request.user.last_name,
                                       'email': request.user.email,
                                       'twitter': form.twitter,
                                       'home_address': form.home_address,
                                       'phone_number': form.phone_number,
                                       'url': form.url,
                                       'notes': form.notes,
                                       },)

    updated = False
    # clear errors
    errors = []
    # up = get_object_or_404(UserProfile, user=request.user)
    print "entry in to account settings"
    try:
       up = UserProfile.objects.get(user=request.user)
       # check for a UserProfile  - set Create to False if one exists
       print "update" 
       create=False
    except(UserProfile.DoesNotExist):
       create=True
       # We failed to get a profile so we set create to True
   
    #  profile = request.user.get_profile()
    if request.method == 'POST':
         form = UserProfileDisplay(request.POST)
         if form.is_valid():
            print "Valid form"
            # we got valid form data back
            data = form.cleaned_data
            
            request.user.first_name= data['first_name']
            request.user.last_name= data['last_name']
            request.user.save()
            
            if create==True:
                # We need to create a UserProfile record and post the valid form data
                up=UserProfile.objects.create(user=request.user)

                up.twitter = data['twitter']
                up.phone_number= data['phone_number']
                up.notes = data['notes']
                up.home_address = data['home_address']
                up.url = data['url']
                up.save()
                messages.info(request,'Your account settings have been created.')  
                #Add RESTCat Update Here
            else:
                # create was false so we need to update an existing profile record
                print "what was that email:"
                user_id = request.user.id
                user = User.objects.get(pk = user_id)
                old_email = user.email
                print "old:" + old_email
                print "new:" + data['email']
                print "now test"
                if (old_email != data['email']):
                    # email was changed so we have to update the original user account
                    user.email = data['email']
                    user.save()
                up.twitter = data['twitter']
                up.phone_number= data['phone_number']
                up.home_address= data['home_address']
                up.notes = data['notes']
                up.url = data['url']
                up.save()
                messages.info(request,'Your account settings have been updated.')

                # We are done we can return to the home page
                return HttpResponseRedirect(reverse('home'),)

            #request.user.message_set.create(
            #    message='Your account settings have been updated.')
            #message='Your account settings have been updated.'
            return render_to_response('accounts/account_settings.html',
                              RequestContext(request,
                                             {'form': form,
                                              'user': request.user,
                                              'page_heading': 'Edit Profile',
                                              'editmode': True,
                                              },))
         else:
            # The form was not valid so we need to re-display the form
            user = User.objects.get(pk = user_id)
            user.userprofile = get_or_create_profile(user)
            form = request.user.get_profile()
            form = UserProfileDisplay(request.POST, initial={'username': request.user,
                                           'first_name': request.user.first_name,
                                           'last_name': request.user.last_name,
                                           'email': request.user.email,
                                           'twitter': form.twitter,
                                           'home_address': form.home_address,
                                           'phone_number': form.phone_number,
                                           'url': form.url,
                                           'notes': form.notes,})
            print "hit the else - we had errors"
            return render_to_response('accounts/account_settings.html',
                                        RequestContext(request,
                                                       {'form': form,
                                                        'user': request.user,
                                                        'editmode': True,
                                                        'page_heading': "Re-Edit Profile",
                                                        },))
             
    else:
        # First time in so we need to display the form
        print "if GET account_settings_else"
        # This is the view step
        user_id = request.user.id
        user = User.objects.get(pk = user_id)
        user.userprofile = get_or_create_profile(user)

        print user.userprofile
        print user_id
        print "user follows:"
        print user
        form.first_name = user.first_name
        form.last_name = user.last_name
        form.email = user.email
        form.twitter = user.userprofile.twitter
        form.home_address = user.userprofile.home_address
        form.phone_number = user.userprofile.phone_number
        form.url = user.userprofile.url
        form.notes = user.userprofile.notes
        
        form = UserProfileDisplay(request.POST, initial={'username': request.user,
                                           'first_name': form.first_name,
                                           'last_name': form.last_name,
                                           'email': form.email,
                                           'twitter': form.twitter,
                                           'home_address': form.home_address,
                                           'phone_number': form.phone_number,
                                           'url': form.url,
                                           'notes': form.notes,
                                           },)


#        print form.first_name + "..." + form.last_name + "..." + form.email

        if create!=True:
            # We are in the display phase but there is a UserProfile
            # so we need to get the data and populate the form
            print "GET but create is false"
                
            form.phone_number = user.userprofile.phone_number
            form.twitter = user.userprofile.twitter
            print form.phone_number
            print "twitter:" + form.twitter


        user_id = request.user.id
        user = User.objects.get(pk = user_id)
        user.userprofile = get_or_create_profile(user)

        print user.userprofile
        print user_id
        print "user follows after GET but create is false:"
        print user
        form.first_name = user.first_name
        form.last_name = user.last_name
        form.email = user.email
        form.twitter = user.userprofile.twitter
        form.home_address = user.userprofile.home_address
        form.phone_number = user.userprofile.phone_number
        form.url = user.userprofile.url
        form.notes = user.userprofile.notes
        print form.email
        print form.notes

        form = UserProfileDisplay( initial={'username': request.user,
                                           'first_name': form.first_name,
                                           'last_name': form.last_name,
                                           'email': form.email,
                                           'twitter': form.twitter,
                                           'home_address': form.home_address,
                                           'phone_number': form.phone_number,
                                           'url': form.url,
                                           'notes': form.notes,
                                           },)
        #{'last_name':form.last_name,
        #                            'first_name': form.first_name,
        #                            'email': form.email,
        #                            'phone_number': form.phone_number,
        #                            'twitter': form.twitter,
        #                            }
        # print form
        print "render response after request.post"
        return render_to_response('accounts/account_settings.html',
                                  RequestContext(request,
                                                 {'form': form,
                                                  'user': request.user,
                                                 'page_heading': 'Edit Profile',
                                                 'editmode': True,
                                                 },))




def verify_email(request, verification_key,
                 template_name='accounts/activate.html',
                 extra_context=None):
    verification_key = verification_key.lower() # Normalize before trying anything with it.
    account = verify(verification_key)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'account': account},
                                context_instance=context)


def get_or_create_profile(user):
    try:
        profile = user.get_profile()
    except ObjectDoesNotExist:
        #create profile - CUSTOMIZE THIS LINE TO OYUR MODEL:
        profile = UserProfile(user=user)
        profile.save()
    return profile
