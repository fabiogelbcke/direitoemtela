from django.db import models
from videos.models import Video
from image_cropping import ImageRatioField, ImageCropField
from .managers import VideoCategoryManager
from django.core.validators import MinValueValidator

# Create your models here.

def get_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('photos', str(instance.id), filename)

class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, blank=True)
    description = models.TextField(blank=True)
    profile_image = ImageCropField(upload_to=get_image_path, blank=True,
                                   default='logodefault.png')
    profile_ratio = ImageRatioField('profile_image', '320x320')
                                   

class Category(models.Model):
    """
    represents the categories (i.e. subjects of the lessons)
    """
    id = models.AutoField(primary_key=True)
    #videos = models.ManyToManyField(Video,
    #                                through='VideoCategory',
    #                                related_name='categories')
    name = models.CharField(max_length=30, blank=True)


class VideoCategory(models.Model):
    """"
    relationship between videos and the categories they're in
    """
    video = models.ForeignKey(Video)
    category = models.ForeignKey(Category)
    position = models.IntegerField(validators=[MinValueValidator(0),])
    objects = VideoCategoryManager()
    
    
