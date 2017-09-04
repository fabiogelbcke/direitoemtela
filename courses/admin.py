from django.contrib import admin
from django import forms

from .models import Course, CourseTopic, CourseItem

from videos.models import Video
from readings.models import Reading
from coursetests.models import CourseTest

from image_cropping import ImageCroppingMixin

class TopicInlineAdmin(admin.TabularInline):
    model = CourseTopic

    
class CourseItemForm(forms.ModelForm):
    video = forms.ModelChoiceField(queryset=Video.objects.order_by('title'))
    test = forms.ModelChoiceField(queryset=CourseTest.objects.order_by('title'))
    reading = forms.ModelChoiceField(queryset=Reading.objects.order_by('title'))
    
    class Meta:
        model = CourseItem
        exclude = []

    
class ItemInlineAdmin(admin.TabularInline):
    model = CourseItem
    form = CourseItemForm


class CourseAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Course
    list_display = ('id', 'name')
    inlines = [TopicInlineAdmin, ItemInlineAdmin]
    
admin.site.register(Course, CourseAdmin)
# Register your models here.
