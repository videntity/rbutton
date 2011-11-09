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
    url(r'^$', direct_to_template, {'template': 'index.html'},  name="home"),
    
    url(r'^upload$', 'rbutton.apps.uploadblue.views.upload', name='upload'),
    
    url(r'^upload-success/(?P<filename>\S+)$',
        'rbutton.apps.uploadblue.views.upload_success', name='upload_success'),
    
    url(r'^accounts/', include('rbutton.apps.accounts.urls')),    
    
    url(r'^download-reformat/(?P<filename>\S+)$',
        'rbutton.apps.uploadblue.views.download_reformat', name='download_reformat'),
   
   url(r'^donate-my-data/(?P<filename>\S+)$',
        'rbutton.apps.uploadblue.views.donate_my_data', name='donate_my_data'),
   
   url(r'^novartis-question/(?P<filename>\S+)$',
        'rbutton.apps.uploadblue.views.novartis_question', name='novartis_question'),
   
   url(r'^novartis-thanks/(?P<filename>\S+)$',
        'rbutton.apps.uploadblue.views.novartis_thanks', name='novartis_thanks'),
	
    url(r'^Intro.html$', direct_to_template, {'template' : 'Intro.html'}),
   		
	url(r'^Privacy.html$', direct_to_template, {'template' : 'Privacy.html'}),	
   
   url(r'^SupportUs.html$', direct_to_template, {'template' : 'SupportUs.html'}),
   
   url(r'^JoinRegistry.html$', direct_to_template, {'template' : 'JoinRegistry.html'}),
                                                    
   url(r'^registry/', include('rbutton.apps.registry.urls')),                                                     
   
   url(r'^tos.html$', direct_to_template, {'template' : 'tos.html'}),
   
   
                       
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

