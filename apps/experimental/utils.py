__author__ = 'mark'
# utils

from string import find



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
    ## ua = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3'


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
    ## ua = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3'

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

