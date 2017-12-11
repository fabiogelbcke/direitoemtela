from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

from .forms import ProfilePicForm


@login_required
def account_page(request):
    profile_pic_form = ProfilePicForm(instance=request.user)
    return render(
        request,
        'account.djhtml',
        {'profile_pic_form': profile_pic_form}
    )


class CustomPasswordResetView(PasswordResetConfirmView):
    template_name = 'reset-password-page.djhtml'
    success_url = reverse_lazy('password_reset_done')
