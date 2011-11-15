#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
# from django.contrib.admin import widgets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.localflavor.us.forms import *
from django.contrib.localflavor.us.models import PhoneNumberField
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.forms import ModelForm
from django.forms.util import ErrorList
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import HttpResponseNotAllowed,  HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.list_detail import object_list
from models import *
from django import forms

class RegistryForm(ModelForm):
    class Meta:
        model = Organization
        exclude = ('status', 'linked_owner')

    
    def save(self, profile_callback=None):
        Organization.save()
        
        return name

    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(RegistryForm, self).save(commit=False)
        if m.status == '':
            m.status = 'pending'
        if m.linked_owner == '':
            m.linked_owner = request.user
        if commit:
            m.save()
        return m


class RegistryFullForm(ModelForm):
    class Meta:
        model = Organization

    def save(self, profile_callback=None):
        Organization.save()

        return name


