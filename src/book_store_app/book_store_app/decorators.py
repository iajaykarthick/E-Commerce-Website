from django.http import HttpResponseRedirect

def my_login_required(function):
    def wraper(request, *args, **kwargs):
        #Check if the Session exists the login key.Here the user_id
        if 'user_id' not in request.session.keys():    
            return HttpResponseRedirect('/login')
        
        elif request.session['user_id'] == 'admin':
            return HttpResponseRedirect('/admin-page')
        else:
            return function(request, *args, **kwargs)

    wraper.__doc__=function.__doc__
    wraper.__name__=function.__name__
    return wraper


def admin_login_required(function):
    def wraper(request, *args, **kwargs):
        #Check if the Session exists the login key.Here the user_id
        if 'user_id' not in request.session.keys():    
            return HttpResponseRedirect('/login')
        
        elif request.session['user_id'] != 'admin':
            return HttpResponseRedirect('/login')
        else:
            return function(request, *args, **kwargs)

    wraper.__doc__=function.__doc__
    wraper.__name__=function.__name__
    return wraper
