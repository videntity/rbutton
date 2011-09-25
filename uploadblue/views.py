# Create your views here.
import os
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings
from forms import UploadForm, SelectFilterForm
from django.core.urlresolvers import reverse
from utils import handle_uploaded_file
from bluebutton.parse import *



def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():  
            filename=handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('upload_success',
						args=(filename, )))

    return render_to_response('upload.html', {'form':UploadForm},
                              RequestContext(request))


def upload_success(request, filename):
    
    
    outfile="%s.json" % (filename)
    filepath=os.path.join(settings.MEDIA_ROOT,filename)
    items = simple_parse(filepath, outfile)
    
    
    demodict = build_simple_demographics_readings(items)
    print demodict
    
    
    if request.method == 'POST':
        form = SelectFilterForm(request.POST)
        if form.is_valid():  
            print "Valid"
            return HttpResponseRedirect(reverse('download_reformat',
						args=(filename, )))

    return render_to_response('select-filter.html',
				{'form':SelectFilterForm,
				 'first_name': demodict['first_name'],
				 'last_name': demodict['last_name']},
                              RequestContext(request))
