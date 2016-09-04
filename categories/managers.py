from django.db import models
from videos.models import Video
from django.core.exceptions import ValidationError

class VideoCategoryManager(models.Manager):
    def create_object(self, video, category,
                      position=None):
        category_count = self.filter(category=category).count() + 1
        if position is None or position >= category_count:
            position = category_count
        elif position <= 0:
            raise ValidationError('Invalid Position. Must be >= 1')
        else:
            pos_change = self.filter(category=category,
                                     position__gte=position)
            for obj in pos_change:
                obj.position += 1
                obj.save()
        vidcat = self.create(video=video,
                             category=category,
                             position=position)
        return vidcat
        
