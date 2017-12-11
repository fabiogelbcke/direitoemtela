from django.contrib import admin
from .models import Video, Tag, ComplementaryMaterial
from image_cropping import ImageCroppingMixin

class ComplementaryMaterialAdmin(admin.TabularInline):
    model = ComplementaryMaterial
    

class VideoAdmin(ImageCroppingMixin, admin.ModelAdmin):
    model = Video
    list_display = ('id', 'title', 'description', 'yt_id', 'date_created')
    inlines = [ComplementaryMaterialAdmin,]
    search_fields = ('title', )
    
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('video', 'name')


admin.site.register(Video, VideoAdmin)
admin.site.register(Tag, TagAdmin)
