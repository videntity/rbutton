#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import *


urlpatterns = patterns('',

    url(r'update/', registry_settings,  name='registry_settings'),
 	url(r'insert/', signup, name='signup'),
    url(r'profile/', registry_settings, name='registry_settings'),
    
    )