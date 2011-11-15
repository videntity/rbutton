#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *
from django.conf.urls.defaults import *
from django.views.generic import ListView
from models import *



organization_info = {
    'queryset': Organization.objects.all(),   
    'template_name': 'registry/organization_list.html',
  #  'template_object_name': 'organization',
}     



urlpatterns = patterns('',

    (r'list/$', ListView.as_view(queryset=Organization.objects.order_by("name"), context_object_name="organization_list")),

    (r'list/approved/$', ApprovedListView.as_view() ),

    url(r'update/', registry_settings,  name='registry_settings'),   
    
 	url(r'insert/', signup, name='signup'),
    url(r'profile/', registry_settings, name='registry_settings'),
    
    )