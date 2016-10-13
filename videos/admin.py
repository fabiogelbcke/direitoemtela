from django.contrib import admin
from .models import Video, Tag
from image_cropping import ImageCroppingMixin

class VideoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'yt_id', 'date_created')

class TagAdmin(admin.ModelAdmin):
    list_display = ('video', 'name')


admin.site.register(Video, VideoAdmin)
admin.site.register(Tag, TagAdmin)
