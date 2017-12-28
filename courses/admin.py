from django.contrib import admin
from django import forms

from .models import Course, CourseTopic, CourseItem, UserCourseRelationship

from videos.models import Video
from readings.models import Reading
from coursetests.models import CourseTest

from image_cropping import ImageCroppingMixin

class TopicInlineAdmin(admin.TabularInline):
    model = CourseTopic

    
class ItemInlineAdmin(admin.TabularInline):
    model = CourseItem
    ordering = ('position',)


class CourseAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Course
    list_display = ('id', 'name')
    inlines = [TopicInlineAdmin, ItemInlineAdmin]

class UserCourseRelationshipAdmin(admin.ModelAdmin):
    model = UserCourseRelationship
    list_display = ('user', 'course', 'start_date', 'completion_date',
                    'completed', 'passed')
    
admin.site.register(Course, CourseAdmin)

admin.site.register(UserCourseRelationship, UserCourseRelationshipAdmin)
# Register your models here.
