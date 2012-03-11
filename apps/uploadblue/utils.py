import uuid, os
from django.conf import settings
from string import find

def handle_uploaded_file(f, myuuid=str(uuid.uuid4())):
    dest_dir=settings.MEDIA_ROOT
    dest_filename="%s.bb" % (myuuid)
    dest_path=os.path.join(dest_dir, dest_filename)
    destination = open(dest_path, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return dest_filename


def de_duplicate_list(list_source):
    list_target = []
    for item in list_source:
        if item not in list_target:
            list_target.append(item)

    return list_target
# Mark Scrimshire:
# Remove duplicate items from a list

def is_iOS(request):
    """
    Attempt to check for iOS as web browser
    """

    #print "META:"
    # print request.META

    print "User Agent:"
    print request.META['HTTP_USER_AGENT']

    ua = request.META['HTTP_USER_AGENT']

    # testing
    ua = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3'


    browser_agent = ""
    is_iOS_test = False

    test_list= [{'char_check':"Safari",'eval_check':False},
                {'char_check':"Mobile",'eval_check':True},
                {'char_check':"iPhone",'eval_check':True},
                {'char_check':"iPod",'eval_check':True},
                {'char_check':"iPad",'eval_check':True}]

    for t in test_list:
        if (find(ua,t['char_check'])> -1):
            print t['char_check']+" "
            browser_agent = browser_agent + t['char_check'] + " "
            if is_iOS_test!=True:
                if t['eval_check']==True:
                    is_iOS_test = True

    print "Browser discovery: "+browser_agent

    if is_iOS_test==True:
        browser_agent = "TRUE:"+browser_agent
    else:
        browser_agent = "FALSE:"+browser_agent

    print "Browser discovery: "+browser_agent

    return is_iOS_test

def is_iOS_browser(request):
    """
    Attempt to check for iOS as web browser
    """

    #print "META:"
    # print request.META

    print "User Agent:"
    print request.META['HTTP_USER_AGENT']

    ua = request.META['HTTP_USER_AGENT']

    # testing
    ua = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3'

    print "testing with:"
    print ua

    browser_agent = ""
    is_iOS_test = False

    test_list= [{'char_check':"Safari",'eval_check':False},
            {'char_check':"Mobile",'eval_check':True},
            {'char_check':"iPhone",'eval_check':True},
            {'char_check':"iPod",'eval_check':True},
            {'char_check':"iPad",'eval_check':True}]

    print test_list


    for t in test_list:
        if (find(ua,t['char_check'])> -1):
            print t['char_check']+" "
            browser_agent = browser_agent + t['char_check'] + " "
            if is_iOS_test!=True:
                if t['eval_check']==True:
                    is_iOS_test = True

    print "Browser discovery: "+browser_agent

    if is_iOS_test==True:
        browser_agent = "TRUE:"+browser_agent
    else:
        browser_agent = "FALSE:"+browser_agent

    print "Browser discovery: "+browser_agent

    return browser_agent

