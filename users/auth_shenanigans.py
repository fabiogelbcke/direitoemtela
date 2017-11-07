from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from urllib import quote_plus

def logout_function(request):
    logout(request)
    if request.GET.get('next', None):
        return redirect(request.GET.get('next'))
    return redirect('/')
    

def email_login(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    print email
    print password
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        next_page = request.GET.get('next', 'index')
        return redirect(next_page)
    else:
        referer = request.META.get('HTTP_REFERER', 'index')
        response = redirect(referer)
        error_msg = 'Email ou senha incorretos. Tente novamente.'
        response['Location'] += '?login_error=' + quote_plus(error_msg)
        return response
