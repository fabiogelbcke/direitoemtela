from django.contrib import admin
from .models import CourseTest, Question, Alternative

# Register your models here.

class QuestionInlineAdmin(admin.TabularInline):
    model = Question

class AlternativeInlineAdmin(admin.TabularInline):
    model = Alternative

class CourseTestAdmin(admin.ModelAdmin):
    model = CourseTest
    list_display = ('title',)
    inlines = [QuestionInlineAdmin,]

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ('text',)
    inlines = [AlternativeInlineAdmin,]

admin.site.register(CourseTest, CourseTestAdmin)
admin.site.register(Question, QuestionAdmin)
