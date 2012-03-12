"""
    Testing picup
"""
from rbutton.apps.experimental.utils import is_iOS, is_iOS_browser, utils_available
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import escape

def browser_test(request):

    received = request
    bt = is_iOS(received)

    print utils_available()

    print "Testing for Safari Mobile Browser:"
    print bt

    ba = is_iOS_browser(received)

    fu = ""

    picup_debug  = "True"
    favicon_url  = escape("http://www.ekive.com/static/rbutton/mainstatic/img/favicon.ico")
    purpose_text = "Upload%20a%20DC%20Medicaid%20Form%20Page"
    callback_url = "http://www.rainbowbutton.com/experiment/upload-done/"
    callback_parameters = "referrername=Picup%20Scratchpad&referrerfavicon="+favicon_url+"&purpose="+purpose_text+"&debug="+picup_debug+"&returnstatus=true&returnserverresponse=true&returnthumbnaildataurl=true&thumbnailsize=50"
    scratch_url  = "fileupload://new?callbackURL="+callback_url+"&"+callback_parameters


    return render_to_response('experimental/evaluate.html',
            {
            'picup_debug': picup_debug,
            'result':bt,
            'found':ba,
            'file_upload': fu,
            'scratch_url': scratch_url,
            'callback_url':callback_url,
            },
        RequestContext(request))


def photo_upload_done(request):
    """
    Return control from iPhone Photo upload to this routine
    """



    return render_to_response('experimental/upload_done.html',
            {

            },
        RequestContext(request))