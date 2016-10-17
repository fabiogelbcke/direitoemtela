from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def channel_views():
    youtube = build(
        settings.YOUTUBE_API_SERVICE_NAME,
        settings.YOUTUBE_API_VERSION,
        developerKey=settings.YT_KEY)
    response = youtube.channels().list(
        id=settings.YT_CHANNEL_ID,
        part="snippet,"
        ).execute()
    print response
    
