#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

# apps.registry

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from datetime import datetime
from registration.models import RegistrationProfile
from models import Organization
from forms import RegistryForm, RegistryFullForm
from django.views.generic import ListView, DetailView


@login_required
def signup(request):
        return render_to_response('registry/insert.html',  RequestContext(request,))
    
    

@login_required
def registry_settings(request):
    message = "default message"
    updated = False
    if request.method == 'POST':
        form = RegistryForm(request.POST)
        if form.is_valid():

            # Create, but don't save the new organization instance.
            new_org = form.save(commit=False)
            # Modify the author in some way.
            new_org.linked_owner = request.user
            new_org.status = 'pending'

            # Save the new instance.
            new_org.save()
            # Now, save the many-to-many data for the form.
            form.save_m2m()

            messages.info(request, 'Your Registry entry has been updated.')
            
            
            return render_to_response('registry/registry_view.html',
                              RequestContext(request,
                                             {'form': form,
                                            
                                              }))
        else:

            print "Form was not valid"
            print form
            print form._errors

            messages.info(request, '')
            print "here" 
            return render_to_response('registry/registry_settings.html',
                                      RequestContext(request,{'form': form,}))
    else:
        form = RegistryForm(request.POST)
        print form
        message='Organization and Organization Type not unique [ organization.name + ' \
        + 'organization.type ]'
        print "in the last else"
    return render_to_response('registry/registry_settings.html',
                              RequestContext(request,
                                             {'form': form, 'updated': message }))

class ApprovedListView(ListView):

    context_object_name = "organization_approved_list"
    queryset = Organization.objects.filter(status="approved")
    template_name = "registry/organization_list.html"


# APPROVAL_CHOICES =( ('pending',  'Pending'),
#                         ('approved',  'Approved'),
#                         ('rejected',  'rejected'),)
