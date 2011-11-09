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
from registration.models import RegistrationProfile
from models import Organization
from forms import RegistryForm    
from django.contrib.localflavor.us.models import PhoneNumberField


from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime

@login_required
def signup(request):
        return render_to_response('registry/insert.html',  RequestContext(request,))
    
    

@login_required
def registry_settings(request):
    updated = False
    if request.method == 'POST':
        form = RegistryForm(request.POST)
        if form.is_valid():
            organization = Organization() 
            organization.organization_linked_user = User
            data = form.cleaned_data
            organization.organization_name = data['organization_name']
            organization.twitter = data['twitter']
            organization.phone_number= data['phone_number']
            organization.save()
            
            message='Your Registry entry has been updated.'
            request.user.message_set.create(
                message='Your Registry entry has been updated.')
            message='Your Registry submission has been updated.'
            return render_to_response('registry/registry_view.html',
                              RequestContext(request,
                                             {'form': form,
                                              'organization': organization_name,
                                              'updated' : message
                                              }))

    else:
        form = RegistryForm()

    return render_to_response('registry/registry_settings.html',
                              RequestContext(request,
                                             {'form': form, }))

