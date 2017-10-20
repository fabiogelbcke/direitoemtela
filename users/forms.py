from django import forms
from .models import MyUser
from image_cropping import ImageCropWidget

class UserForm(forms.ModelForm):
    #city = forms.CharField(required=False)
    #state = forms.CharField(required=False)
    
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email']#, 'city', 'state']

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['profile_image',]

class CropProfilePicForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['profile_image', 'profile_ratio']
