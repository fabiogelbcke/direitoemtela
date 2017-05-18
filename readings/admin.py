from django.contrib import admin
from .models import Reading

class ReadingAdmin(admin.ModelAdmin):
    model = Reading


admin.site.register(Reading, ReadingAdmin)

