# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings

def home(request):
    return render_to_response('index.html', {'first_name':"Mark",
				'last_name':'Scrimshire',},
                              RequestContext(request))
