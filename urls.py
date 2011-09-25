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
    url(r'^upload$', 'rbutton.uploadblue.views.upload', name='upload'),
    url(r'^upload-success/(?P<filename>\S+)$',
        'rbutton.uploadblue.views.upload_success', name='upload_success'),
   
    url(r'^download-reformat/(?P<filename>\S+)$',
        'rbutton.uploadblue.views.download_reformat', name='download_reformat'),
   
   url(r'^donate-my-data/(?P<filename>\S+)$',
        'rbutton.uploadblue.views.donate_my_data', name='donate_my_data'),
   
   url(r'^novartis-question/(?P<filename>\S+)$',
        'rbutton.uploadblue.views.novartis_question', name='novartis_question'),
   
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

