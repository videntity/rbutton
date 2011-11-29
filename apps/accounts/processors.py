__author__ = 'mark'
from models import Permission, UserProfile
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404



def display(request):
    print "reached display contaxt proc"

    if hasattr(request, 'user'):
        print "inside the first if of context proc"
        if request.user.is_authenticated():
            print "user is authenticated in context proc"
            print request.user
            u = get_object_or_404(UserProfile, user=request.user)

            print u
            d = u.display
            print d
            return {'display': d }
    return {}