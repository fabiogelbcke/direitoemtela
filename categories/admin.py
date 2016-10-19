from django.contrib import admin
from .models import Category, VideoCategory, Professor
from image_cropping import ImageCroppingMixin

class VideoCategoryInline(admin.TabularInline):
    model = VideoCategory
    ordering = ['position']
    

class CategoryAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'yt_id', 'featured', 'hidden')
    fields = ['title', 'yt_id', 'featured', 'professor', 'description', 'thumbnail', 'thumbnail_ratio', 'hidden']
    inlines = [VideoCategoryInline,]

class ProfessorAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Professor, ProfessorAdmin)
