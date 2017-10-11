# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest

from .forms import UserForm, ProfilePicForm
from .models import MyUser
from .validators import validate_password

@login_required
def update_user_info(request):
    form = UserForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        return HttpResponse('Salvo!')
    return HttpResponseBadRequest(
        'Dados inválidos. Por favor verifique '
        'as informações digitadas e tente novamente.'
    )


@login_required
def change_password(request):
    user = request.user
    password = request.POST.get('password', '')
    password_confirmation = request.POST.get('password_confirmation', '')
    if (password != password_confirmation):
        return HttpResponseBadRequest('A senha e a confirmação não batem!')
    if validate_password(password) is False:
        return HttpResponseBadRequest(
            'A senha deve ter ao menos 8 caracteres, '
            'entre eles uma letra e um número!'
        )
    
    user.set_password(password)
    user.save()
    return HttpResponse('Senha Alterada!')


@login_required
def upload_new_photo(request):
    user = request.user
    pic_form = ProfilePicForm(
        request.POST,
        request.FILES,
        instance=user
    )
    print request.POST
    print request.FILES
    if pic_form.is_valid():
        user.profile_picture = request.FILES['profile_picture']
        user.save()
        print 'oi'
        return HttpResponse('Foto Salva')
    return HttpResponseBadRequest('Imagem Inválida')
