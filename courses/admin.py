from django.contrib import admin
from .models import Course, CourseTopic, CourseItem
from image_cropping import ImageCroppingMixin

class TopicInlineAdmin(admin.TabularInline):
    model = CourseTopic

class ItemInlineAdmin(admin.TabularInline):
    model = CourseItem

class CourseAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Course
    list_display = ('id', 'name')
    inlines = [TopicInlineAdmin, ItemInlineAdmin]
    
admin.site.register(Course, CourseAdmin)
# Register your models here.
