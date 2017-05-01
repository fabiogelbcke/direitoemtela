# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from image_cropping import ImageRatioField, ImageCropField
import uuid
import os
import shortuuid

def get_thumbnail_path(instance, filename):
    return os.path.join('thumbnails', str(instance.id), shortuuid.uuid())

def get_material_path(instance, filename):
    return os.path.join('materials', shortuuid.uuid())

class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    yt_id = models.TextField(max_length=20, blank=True)
    yt_title = models.CharField(max_length=300, blank=True)
    published_at_yt = models.DateTimeField(null=True)
    date_created = models.DateTimeField(default=timezone.now)
    thumbnail = ImageCropField(upload_to=get_thumbnail_path,
                               blank=True,
                               default='logodefault.png')
    thumbnail_ratio = ImageRatioField('thumbnail', '1600x900')
    yt_lesson_number = models.CharField(max_length=4, blank=True)
    professor = models.ForeignKey('categories.Professor',
                                  related_name='videos',
                                  null=True)

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video, related_name='tags')
    name = models.CharField(max_length=100, blank=True)


class ComplementaryMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video,
                              related_name='complementary_materials',
                              null=True,
                              default=None)
    title = models.CharField(max_length=200, default='')
    url = models.CharField(max_length=300,
                           blank=True,
                           default='')
    material_file = models.FileField(upload_to=get_material_path,
                                     blank=True,
                                     null=True,
                                     default=None)

    def is_link(self):
        return bool(self.url)

    def is_file(self):
        return bool(self.material_file)
