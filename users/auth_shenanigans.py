from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_function(request):
    logout(request)
    if request.GET.get('next', None):
        return redirect(request.GET.get('next'))
    return redirect('/')
    
