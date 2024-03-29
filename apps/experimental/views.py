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
    favicon_url  = "http%3A//www.ekive.com/static/rbutton/mainstatic/img/favicon.ico"
    purpose_text = "Upload%20a%20DC%20Medicaid%20Form%20Page"
    callback_url = "http://www.rainbowbutton.com/experiment/upload-done/"
    callback_parameters = "referrerName=RainbowButton%20Upload&referrerFavicon="+favicon_url+"&purpose="+purpose_text+"&debug="+picup_debug+"&returnStatus=true&returnServerResponse=true&returnThumbnailDataurl=true&thumbnailSize=50"
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


def photo_upload_save(request):
    """
    Return with hash parameters
    """
    received = request
    print received
    bt = is_iOS(received)

    print utils_available()

    print "Testing for Safari Mobile Browser:"
    print bt

    ba = is_iOS_browser(received)

    remoteImageURL = request.GET['remoteImageURL']

    fu = ""
    fu = fu + remoteImageURL

    return render_to_response('experimental/evaluate.html',
            {

            'result':bt,
            'found':ba,
            'file_upload': fu,
            'post_processing':"True",

            },
            RequestContext(request))