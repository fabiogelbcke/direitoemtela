# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

# Create your models here.
class CourseTest(models.Model):
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(default='',
                             blank=True,
                             max_length=150)
    ref = models.CharField(default='',
                           blank=True,
                           max_length=150,
                           unique=False)

    def __str__(self):
        return self.ref

    def __unicode__(self):
        return self.ref

    class Meta:
        verbose_name = 'Teste'
        verbose_name_plural = 'Testes'
        ordering = ['title',]

class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('correct', 'correta'),
        ('incorrect', 'incorreta'),
        ('tof', 'V ou F'),
    )
    
    id = models.AutoField(primary_key=True)
    test = models.ForeignKey(CourseTest,
                             related_name='questions')
    text = models.CharField(default='',
                            blank=True,
                            max_length=250)
    users = models.ManyToManyField(settings.SOCIAL_AUTH_USER_MODEL,
                                   through='UserQuestionRelationship',
                                   related_name='questions')
    answer_type = models.CharField(max_length=15,
                                   choices=QUESTION_TYPE_CHOICES,
                                   default='correct')

    class Meta:
        verbose_name = 'Questão'
        verbose_name_plural = 'Questões'
        ordering = ['text',]

class Alternative(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question,
                                 related_name='alternatives')
    correct = models.BooleanField(default=False)
    text = models.TextField(default='')

class UserQuestionRelationship(models.Model):
    user = models.ForeignKey(settings.SOCIAL_AUTH_USER_MODEL)
    question = models.ForeignKey(Question)
    answered = models.BooleanField(default=False)
    answered_correctly = models.BooleanField(default=False)
