# Create your views here.
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from forms import BlueButtonFileUploadForm, SelectFilterForm, NovartisForm, DonateForm, SubmitDataRecipientRequestForm
from utils import handle_uploaded_file, de_duplicate_list
from bluebutton.parse import *
from djangomodels2xls import convert2excel, simpler_parse
import urllib2
import json
import re

from apps.registry.models import Organization, Trigger


def upload(request):
    print "STATIC_URL / STATIC_ROOT / STATICFILES_DIRS"
    print settings.STATIC_URL
    print settings.STATIC_ROOT
    print settings.STATICFILES_DIRS
    print settings.SITE_URL
    
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
    # Let's look at the contents of items
    file_review = open(filepath, 'r').read()
    u_file_review = file_review.upper()

    print u_file_review
    # try adding code to search file for active triggers

    print "--- TRIGGER"
    trigger_action = Trigger.objects.filter(active='active').values()
    print trigger_action
    for trigger in trigger_action:
        # print trigger.organization
        u_trigger = trigger['trigger'].upper()
        test_compare = re.search(u_trigger, u_file_review)
        print test_compare
        if test_compare !='':
            print "Match"
            org_info = Organization.objects.get(id=trigger['organization_id'])
            organization_name = org_info.name
            alert_msg = "Alert for " + trigger['trigger'] + " from "+ organization_name
            alert_msg = alert_msg +"\n " + trigger['Question']
            messages.success(request, alert_msg)

#        print u_trigger['trigger']
#        print u_trigger['organization_id']
 #       for item in items:
 #           if u_trigger['trigger'] in item['key']:
  #              print item['key']

   #         print "v matches"
    #        if trigger['trigger'] in item['value']:
     #           print item['value']

        

    print "--- END TRIGGER"
    

    # end of trigger search

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
    print "items: (from simple parse)"
    print items

    med_items = simpler_parse(filepath, medsfilefilepath)
    print "items: (from simpler parse):"
    print med_items
    """ generate the information as excel in media"""
    # Basic info
    my_info = build_simple_demographics_readings(items)
    print my_info
    me_data = [my_info,]
    excel_wb_object = convert2excel(me_data,
                                    filename,
                                    'MyInfo',
                                    'open',
                                    '')
    # open and update modes returns Excel_workbook_object
    #add to Excel Sheet

    # Weight Info
    my_weight = build_wt_readings(items)
    print "Weight information:"
    print my_weight
    excel_wb_object = convert2excel(my_weight,
                            filename,
                            'Weight',
                            'update',
                            excel_wb_object)

    # Blood Pressure Info
    my_bp = build_bp_readings(items)
    print "Blood pressure:"
    print my_bp
    excel_wb_object = convert2excel(my_bp,
                                    filename,
                                    'BloodPressure',
                                    'update',
                                    excel_wb_object)

    # Meds info
    meds = build_mds_readings(items)
    print "Meds for Excel File:"
    print meds
    # for some reason the meds routine seems to work
    # dedup meds entries
    de_meds = de_duplicate_list(meds)
    # print "DEDUP THE MEDS..........."
    # print de_meds
    excelfilename = convert2excel(de_meds,
                                  filename,
                                  'Medications',
                                  'save',
                                  excel_wb_object)
    # save mode returns Excel filename
    # modified function to allow customization of worksheet tab name


    print "excel is", excelfilename

    next = '/donate-my-data/' + filename

    return render_to_response('select-Donation.html',
				{
				'filename': filename,
				 'sanitizedfile': sanitized_file,
				 'excelfilename': excelfilename,
                 'next': next,},
                              RequestContext(request))
    
@login_required()
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


