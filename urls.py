#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.STATIC_ROOT}),
    url(r'^$', direct_to_template, {'template': 'index.html'}),
    url(r'^upload$', 'rbutton.uploadblue.views.home', name='upload'),
    url(r'^upload-success/(?P<filename>\S+)$',
        'rbutton.uploadblue.views.upload_success', name='upload_success'),
   

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

