from django import forms
from .models import Reading

class ReadingForm(forms.ModelForm):
    description = forms.CharField(required=False)
    
    class Meta:
        model = Reading
        fields = ['reading_file', 'title', 'description']
