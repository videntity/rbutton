#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from django.db.models import Sum
from models import *
from django import forms
  
#from django.contrib.admin import widgets
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  
from django.forms.util import ErrorList
from django.contrib.localflavor.us.forms import *
from django.conf import settings
from django.contrib.localflavor.us.models import PhoneNumberField

from django.core.urlresolvers import reverse



class RegistryForm(forms.Form):
    organization_name           = forms.CharField(max_length=100, label="Organization Name*")
    organization_contact        = forms.CharField(max_length=100, label="Contact Name*")
    organization_url            = forms.URLField(max_length=150, label="Web Address(URL)")
    organization_email          = forms.EmailField(max_length=100, label="Email")
    organizaton_linked_owner    = 'user.username'
    organization_type           = forms.CharField(max_length=10,
                                               label="Type")
    phone_number                = forms.CharField(max_length=15, label="Phone Number") 
    twitter                     = forms.CharField(max_length=15, label="Twitter")
    notes                       = forms.CharField(max_length=250, label="Notes")


    



    def save(self, profile_callback=None):
        organization.save()
        
        return organization_name

