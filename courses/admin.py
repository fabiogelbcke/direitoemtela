from django.contrib import admin
from .models import Course, CourseTopic, CourseItem

class TopicInlineAdmin(admin.TabularInline):
    model = CourseTopic

class ItemInlineAdmin(admin.TabularInline):
    model = CourseItem

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ('id', 'name')
    inlines = [TopicInlineAdmin, ItemInlineAdmin]
    
admin.site.register(Course, CourseAdmin)
# Register your models here.
