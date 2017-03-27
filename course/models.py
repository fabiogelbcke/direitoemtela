from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(blank=True, max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField()
    professor = models.ForeignKey('categories.Professor',
                                  related_name='courses', null=True)
    hidden = models.BooleanField(default=False)


class CourseItem(models.Model):
    course = models.ForeignKey(Course, related_name='items')
    position = models.IntegerField(validators=[MinValueValidator(0),])
    #types: 1 - video, 2 - reading, 3 - test
    item_type = models.IntegerField()
    video = models.ForeignKey(Video, related_name='course_items')
    #reading = models.ForeignKey(, related_name='course_items')
    #test = models.ForeignKey(Video, related_name='course_items')

class UserItemRelationship(models.Model):
    
