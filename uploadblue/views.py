# Create your views here.
import os
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings
from forms import UploadForm, SelectFilterForm, NovartisForm, DonateForm
from django.core.urlresolvers import reverse
from utils import handle_uploaded_file
from bluebutton.parse import *
from djangomodels2xls import convert2excel


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
    
    if request.method == 'POST':
        form = SelectFilterForm(request.POST)
        if form.is_valid():  
            return HttpResponseRedirect(reverse('download_reformat',
						args=(filename, )))

    return render_to_response('select-filter.html',
				{'form':SelectFilterForm,
				 'filename': filename,
				 'first_name': demodict['first_name'],
				 'last_name': demodict['last_name']},
                              RequestContext(request))



def download_reformat(request, filename, sec_level=1):
    
    """run the reformatter & save sanitized version"""
    filepath=os.path.join(settings.MEDIA_ROOT,filename)
    sanitized_file = "%s.sanitized" % (filename)
    sanitized_path =  os.path.join(settings.MEDIA_ROOT, sanitized_file)
    green_parse(filepath, sanitized_path, sec_level)
    
    """ generate meds information as json in media"""
    items = simple_parse(filepath, "outfile")
    meds = build_mds_readings(items)
    """ generate the information as excel in media"""
    excelfilename = convert2excel(meds)
    print "excel is", excelfilename

    return render_to_response('select-Donation.html',
				{
				'filename': filename,
				 'sanitizedfile': sanitized_file,
				 'exceldownload': excelfilename},
                              RequestContext(request))
    
def donate_my_data(request, filename):
    
    
    if request.method == 'POST':
        form = DonateForm(request.POST)
        if form.is_valid():  
            return HttpResponseRedirect(reverse('novartis_question',
						args=(filename, )))

    return render_to_response('select-research.html',
				{'form':DonateForm,
				 'filename': filename,
				},
                              RequestContext(request))

def novartis_question(request, filename):
    
    vomiting_rate="50%"
    
    
    if request.method == 'POST':
        form = DonaterForm(request.POST)
        if form.is_valid():  
            return HttpResponseRedirect(reverse('novartis_question',
						args=(filename, )))

    return render_to_response('novartis-question.html',
				{
				    'form':NovartisForm,
				    'vomiting_rate': vomiting_rate,
				},
                              RequestContext(request))