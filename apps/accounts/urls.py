#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from rbutton.apps.accounts.views import *
from django_rpx_plus.views import *

#    sms_code, sms_login, mylogout, password_reset_request, reset_password, simple_login, signup, account_settings


urlpatterns = patterns('',

    url(r'login/', simple_login,  name='simple_login'),
    url(r'smscode/', sms_code, name='sms_code'),
    url(r'logout/', mylogout, name='mylogout'),
    url(r'password-reset-request/', password_reset_request,
        name='password_reset_request'),     
	url(r'signup/', signup, name='signup'),
    url(r'register/', profile, name='profile'),
    url(r'profile/', account_settings, name='account_settings'),
    url(r'reset-password/(?P<reset_password_key>[^/]+)/$', reset_password,
        name='password_reset_request'),
    url(r'social/', socialprofile, name='socialprofile'),
    url(r'rpx_register', 'django_rpx_plus.views.register'),
    url(r'rpx_associate', 'django_rpx_plus.views.associate'),

#    url(r'^accounts/', include('django_rpx_plus.urls')),

    url(r'registration/', registration, name='registration'),


    )