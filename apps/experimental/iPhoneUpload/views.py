__author__ = 'mark'
# Create your views here.
from apps.experimental.utils import is_iOS, is_iOS_browser

def browser_test(request):

    received = request
    bt = is_iOS(received)


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


