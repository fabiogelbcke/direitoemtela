from django.contrib import admin
from .models import MyUser

class CourseInlineAdmin(admin.TabularInline):
    model = MyUser.courses.through

class UserAdmin(admin.ModelAdmin):
    model = MyUser
    list_display = ('id', 'get_full_name', 'email')
    inlines = [CourseInlineAdmin,]

admin.site.register(MyUser, UserAdmin)


# Register your models here.
