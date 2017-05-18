from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.conf import settings
from videos.models import Video
from image_cropping import ImageRatioField, ImageCropField
import shortuuid
from coursetests.models import CourseTest
from readings.models import Reading
import os


def get_thumbnail_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (shortuuid.uuid(), ext)
    return os.path.join('coursethumbnails', str(instance.id), filename)

class Course(models.Model):
    name = models.CharField(blank=True, max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    trailer_url = models.CharField(blank=True, default='', max_length=300)
    professor = models.ForeignKey('categories.Professor',
                                  related_name='courses',
                                  null=True,
                                  blank=True,
                                  default=None)
    hidden = models.BooleanField(default=False)
    hours = models.IntegerField(default=0)
    users = models.ManyToManyField(settings.SOCIAL_AUTH_USER_MODEL,
                                   through='UserCourseRelationship',
                                   related_name='courses')
    thumbnail = ImageCropField(upload_to=get_thumbnail_path, blank=True,
                               default='logodefault.png')
    thumbnail_ratio = ImageRatioField('thumbnail', '592x300')
    total_questions = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            total_questions = 0
            for item in self.items.filter(test__isnull=False):
                total_questions += item.test.questions.all().count()
            self.total_questions = total_questions
        super(Course, self).save(*args, **kwargs)

    def is_registered(self, user):
        return self.course_rels.filter(user=user).exists()

class CourseTopic(models.Model):
    course = models.ForeignKey(Course, related_name='topics')
    text = models.CharField(blank=True, max_length=200)

class CourseItem(models.Model):
    class Meta:
        ordering = ['position',]
        #unique_together = ['course', 'position']

    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, related_name='items')
    position = models.IntegerField(validators=[MinValueValidator(0),])
    #types: 1 - video, 2 - reading, 3 - test
    video = models.ForeignKey(Video,
                              related_name='course_items',
                              null=True,
                              default=None,
                              blank=True)
    title = models.CharField(default='', max_length=150)
    users = models.ManyToManyField(settings.SOCIAL_AUTH_USER_MODEL,
                                   through='UserItemRelationship',
                                   related_name='course_items')
    reading = models.ForeignKey(Reading,
                                related_name='course_items',
                                blank=True,
                                null=True,
                                default=None)
    test = models.OneToOneField(CourseTest,
                                related_name='course_item',
                                default=None,
                                null=True,
                                blank=True)

    def type(self):
        if self.video is not None:
            return 'video'
        elif self.test is not None:
            return 'test'
        elif self.reading is not None:
            return 'reading'

    def save(self, *args, **kwargs):
        position = self.position
        course_count = CourseItem.objects.filter(course=self.course).count()
        if self.pk is None:
            course_count += 1
            pos_diff = 1
            old_position = course_count
        if position is None or position > course_count:
            position = course_count
        if position <= 0:
            raise ValidationError('Invalid Position. Must be >= 1')
        #if video is added in an earlier position than before, move the videos
        #in between the 2 positions 1 position forward. e.g if you move a video
        #from position 8 to position 4, move videos in positions 4,5,6,7 to
        #positions 5,6,7,8. If moving to a later position (or new video being added)
        #do the opposite (decrease 1 position for each) e.g. 5,6,7,8 to 4,5,6,7
        if self.pk is not None:
            old_position = CourseItem.objects.get(id=self.pk).position
            if old_position != position:
                pos_diff = 1 if old_position > position else -1
            else:
                pos_diff = 0
        if pos_diff != 0 and CourseItem.objects.filter(
                course=self.course,
                position__gte=position
        ).exclude(title=self.title).exists():
            #indexes between which positions will change
            obj_change_indexes = [position, old_position - pos_diff]
            pos_change = CourseItem.objects.filter(
                course=self.course,
                position__gte=min(obj_change_indexes),
                position__lte=max(obj_change_indexes)
            ).exclude(video=self.video)
            for obj in pos_change:
                #have to call update cause it doesn't call custom save (direct SQL)
                CourseItem.objects.filter(id=obj.id).update(position=obj.position + pos_diff)
        self.position = position
        super(CourseItem, self).save(*args, **kwargs)

    def delete(self):
        position = self.position
        bigger_positions = CourseItem.objects.filter(
            course=self.course,
            position__gte=position
            ).exclude(video=self.video)
        for viditem in bigger_positions:
            viditem.position = viditem.position - 1
            viditem.save()
        super(CourseItem, self).delete()

class UserItemRelationship(models.Model):
    user = models.ForeignKey(settings.SOCIAL_AUTH_USER_MODEL)
    course_item = models.ForeignKey(CourseItem)
    done = models.BooleanField(default=False)

class UserCourseRelationship(models.Model):
    user = models.ForeignKey(settings.SOCIAL_AUTH_USER_MODEL)
    course = models.ForeignKey(Course, related_name='course_rels')
    correct_answers = models.IntegerField(default=0)
    questions_answered = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    passing_grade = models.IntegerField(default=70)
    completed = models.BooleanField(default=False)
    passed = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now)
    completion_date = models.DateTimeField(null=True,
                                           default=None)
    last_accessed_item = models.ForeignKey(CourseItem,
                                           null=True,
                                           default=None)
    certificate = models.OneToOneField('Certificate',
                                       related_name='course_rel',
                                       null=True,
                                       default=None)

    def percentage(self):
        if self.total_questions == 0:
            return 0
        return int(100 * (1.0*self.correct_answers/self.total_questions))


class Certificate(models.Model):
    user = models.ForeignKey(settings.SOCIAL_AUTH_USER_MODEL,
                             related_name='certificates')
    course_name = models.CharField(max_length=150)
    course_hours = models.IntegerField()
    completion_date = models.DateTimeField(null=True,
                                           default=timezone.now)
    identifier = models.CharField(primary_key=True,
                                  max_length=150,
                                  default=shortuuid.uuid)
    percentage = models.IntegerField()
    
