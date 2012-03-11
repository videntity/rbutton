__author__ = 'mark'

from apps.experimental.utils import is_iOS, is_iOS_browser, utils_available
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Template, Context

def browser_test(request):

    received = request
    bt = is_iOS(received)

    print utils_available()

    print "Testing for Safari Mobile Browser:"
    print bt

    ba = is_iOS_browser(received)

    fu = ""

    return render_to_response('experimental/evaluate.html',
            {
            'result':bt,
            'found':ba,
            'file_upload': fu,


            },
        RequestContext(request))


