# Create your views here.
import os
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.conf import settings
from forms import BlueButtonFileUploadForm, SelectFilterForm, NovartisForm, DonateForm, SubmitDataRecipientRequestForm
from django.core.urlresolvers import reverse
from utils import handle_uploaded_file
from bluebutton.parse import *
from djangomodels2xls import convert2excel
import urllib2
import json
from apps.registry.models import Organization


def upload(request):
    if request.method == 'POST':
        form = BlueButtonFileUploadForm(request.POST, request.FILES)
        if form.is_valid():  
            filename=handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('upload_success',
						args=(filename, )))
	else:
	    return render_to_response('upload.html', {'form':form},
                              RequestContext(request))
    return render_to_response('upload.html', {'form':BlueButtonFileUploadForm},
                              RequestContext(request))


def upload_success(request, filename):
    
    
    outfile="%s.json" % (filename)
    outfilepath=os.path.join(settings.MEDIA_ROOT,outfile)
    filepath=os.path.join(settings.MEDIA_ROOT,filename)
    items = simple_parse(filepath, outfilepath)
    
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
    medsfilefilepath = "%s.meds" % (filepath)
    """ generate meds information as json in media"""
    items = simple_parse(filepath, medsfilefilepath)
    meds = build_mds_readings(items)
    """ generate the information as excel in media"""
    excelfilename = convert2excel(meds, filename)
    print "excel is", excelfilename

    return render_to_response('select-Donation.html',
				{
				'filename': filename,
				 'sanitizedfile': sanitized_file,
				 'excelfilename': excelfilename},
                              RequestContext(request))
    
def donate_my_data(request, filename):
    
    object_list = Organization.objects.filter(status='approved')
    print object_list
    if request.method == 'POST':
        form = DonateForm(request.POST)
        form_selection = request.POST.getlist('select_to_donate')
        print form_selection
        if form.is_valid():  
            return HttpResponseRedirect(reverse('novartis_question',
						args=(filename, )))

    return render_to_response('select-research.html',
				{'form':DonateForm,
				 'filename': filename,
                 'object_list': object_list,
				},
                              RequestContext(request))

def novartis_question(request, filename):
    
    if request.method == 'POST':
        form = NovartisForm(request.POST)
        if form.is_valid():  
            return HttpResponseRedirect(reverse('novartis_thanks',
						args=(filename, )))


    response = urllib2.urlopen('http://spl.anzonow.com/query?uri=http%3A//spl-ld.anzonow.com/data/document1')
    myresponse = response.read()
    myresponse = json.loads(myresponse)
    
    #print myresponse['Adverse_Reaction_Section']['specifics']['3']['reportedAdverseReaction']['2']['summary']
    
    
    mysummary= myresponse['Adverse_Reaction_Section']['specifics'][3]['reportedAdverseReaction'][2]['summary']
    mylabel = myresponse['Adverse_Reaction_Section']['specifics'][3]['reportedAdverseReaction'][2]['label']
    

    return render_to_response('novartis-question.html',
				{
				    'form':NovartisForm,
				    'filename': filename,
				    'mysummary': mysummary,
				    'mylabel': mylabel
				},
                              RequestContext(request))
    
    
def novartis_thanks(request, filename):
    return render_to_response('novartis-thanks.html',
				{'filename':filename},
                              RequestContext(request))

def apply_as_data_recipient(request):
    return render_to_response('apply-as-data-recipient.html',
                              {
                              'form':SubmitDataRecipientRequestForm
                              
                              },
                              RequestContext(request))

