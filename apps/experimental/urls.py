__author__ = 'mark'
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'experimental.views.home', name='home'),
    # url(r'^experimental/', include('experimental.foo.urls')),

    url(r'^iosload/', 'rbutton.apps.experimental.views.browser_test', name='iosupload'),

    url(r'^upload-done/', 'rbutton.apps.experimental.views.photo_upload_done', name='iosdone'),

    url(r'^$', direct_to_template, {'template': 'experimental/index.html'},  name="testhome"),

    url(r'^index.html$', direct_to_template, {'template': 'experimental/index.html'},  name="testhome"),


)
