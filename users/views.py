from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import ProfilePicForm


@login_required
def account_page(request):
    profile_pic_form = ProfilePicForm(instance=request.user)
    return render(
        request,
        'account.djhtml',
        {'profile_pic_form': profile_pic_form}
    )

