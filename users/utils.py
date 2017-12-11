# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash


import string
import json


from .forms import UserForm, ProfilePicForm, CropProfilePicForm
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
    update_session_auth_hash(request, request.user)
    return HttpResponse('Senha Alterada!')


@login_required
def upload_new_photo(request):
    user = request.user
    pic_form = ProfilePicForm(
        request.POST,
        request.FILES,
        instance=user
    )
    if pic_form.is_valid():
        user.profile_image = request.FILES['profile_picture']
        user.save()
        template_body = loader.get_template('picture_crop.djhtml')
        crop_picture_form = CropProfilePicForm(instance=request.user)
        body_data = template_body.render(
            {'crop_picture_form': crop_picture_form,},
            request
        )
        template_head = loader.get_template('picture_crop_head.djhtml')
        head_data = template_head.render(
            {'crop_picture_form': crop_picture_form,},
            request
        )
        print head_data
        head_data = '\n'.join(
            [x for x in head_data.split('\n') if 'jquery-' not in x]
        )
        return HttpResponse(json.dumps(
            {
                'body': body_data,
                'head': head_data
            }
        ))
    else:
        return HttpResponseBadRequest('Imagem Inválida')


@login_required
def save_cropped_photo(request):
    user = request.user
    pic_form = CropProfilePicForm(
        request.POST,
        request.FILES,
        instance=user
    )
    if pic_form.is_valid():
        pic_form.save()
        return redirect('account')
        return HttpResponse('Foto Salva!')
    return HttpResponseBadRequest('Houve um problema ao salvar a foto')
    

def reset_password_confirm(request):
    return True
