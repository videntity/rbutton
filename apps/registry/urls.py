#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from models import Organization

organization_info = {
    'queryset': Organization.objects.all(),   
    'template_name': 'registry/registry_list.html', 
  #  'template_object_name': 'organization',
}     


urlpatterns = patterns('',

    (r'list/$', list_detail.object_list, organization_info),
    
    url(r'update/', registry_settings,  name='registry_settings'),   
    
 	url(r'insert/', signup, name='signup'),
    url(r'profile/', registry_settings, name='registry_settings'),
    
    )