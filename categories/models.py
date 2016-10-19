from django.db import models
from videos.models import Video
from image_cropping import ImageRatioField, ImageCropField
from .managers import VideoCategoryManager
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import shortuuid
import uuid
import os
# Create your models here.

def get_image_path(instance, filename):
    return os.path.join('professorphotos', str(instance.id), shortuuid.uuid())

def get_thumbnail_path(instance, filename):
    return os.path.join('categorythumbnails', str(instance.id), shortuuid.uuid())

class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    profile_image = ImageCropField(upload_to=get_image_path, blank=True,
                                   default='logodefault.png')
    profile_ratio = ImageRatioField('profile_image', '320x320')

    def __unicode__(self):
        return self.name
                                   

class Category(models.Model):
    """
    represents the categories (i.e. subjects of the lessons)
    """
    id = models.AutoField(primary_key=True)
    videos = models.ManyToManyField(Video,
                                    through='VideoCategory',
                                    related_name='categories')
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=300, blank=True)
    yt_id = models.CharField(max_length=100, blank=True)
    featured = models.BooleanField(default=False, blank=True)
    professor = models.ForeignKey(Professor,
                                  related_name='categories',
                                  null=True,
                                  blank=True)
    thumbnail = ImageCropField(upload_to=get_thumbnail_path, blank=True,
                               default='logodefault.png')
    thumbnail_ratio = ImageRatioField('thumbnail', '592x300')
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class VideoCategory(models.Model):
    """"
    relationship between videos and the categories they're in
    """
    video = models.ForeignKey(Video)
    category = models.ForeignKey(Category)
    position = models.IntegerField(validators=[MinValueValidator(0),])
    yt_position = models.CharField(max_length=4, blank=True)
    objects = VideoCategoryManager()

    def save(self, *args, **kwargs):
        position = self.position
        category_count = VideoCategory.objects.filter(category=self.category).count()
        if self.pk is None:
            category_count += 1
            pos_diff = 1
            old_position = category_count
        if position is None or position > category_count:
            position = category_count
        if position <= 0:
            raise ValidationError('Invalid Position. Must be >= 1')
        #if video is added in an earlier position than before, move the videos
        #in between the 2 positions 1 position forward. e.g if you move a video
        #from position 8 to position 4, move videos in positions 4,5,6,7 to
        #positions 5,6,7,8. If moving to a later position (or new video being added)
        #do the opposite (decrease 1 position for each) e.g. 5,6,7,8 to 4,5,6,7
        if self.pk is not None:
            old_position = VideoCategory.objects.get(id=self.pk).position
            if old_position != position:
                pos_diff = 1 if old_position > position else -1
            else:
                pos_diff = 0
        if pos_diff != 0 and VideoCategory.objects.filter(
                category=self.category,
                position__gte=position
        ).exclude(video=self.video).exists():
            #indexes between which positions will change
            obj_change_indexes = [position, old_position - pos_diff]
            pos_change = VideoCategory.objects.filter(
                category=self.category,
                position__gte=min(obj_change_indexes),
                position__lte=max(obj_change_indexes)
            ).exclude(video=self.video)
            for obj in pos_change:
                #have to call update cause it doesn't call custom save (direct SQL)
                VideoCategory.objects.filter(id=obj.id).update(position=obj.position + pos_diff)
        self.position = position
        super(VideoCategory, self).save(*args, **kwargs)
    
