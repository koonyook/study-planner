# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
class Institution(models.Model):
    """(Institution description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return unicode(self.name)
        
class Course(models.Model): #สาขาวิชา
    """(Course description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    units_limit_in_first_semester = models.IntegerField()
    units_limit_in_second_semester = models.IntegerField()
    units_limit_in_summer_semester = models.IntegerField()
    required_free_subject_units = models.IntegerField()
    
    institution = models.ForeignKey('Institution')
    required_subjects = models.ManyToManyField('Subject')
    required_groups = models.ManyToManyField('Group')

    def __unicode__(self):
        return unicode(self.name)

class Subject(models.Model):
    """(Subject description)"""
    #code = models.IntegerField()		#test change name # change to charfield
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    thai_name = models.CharField(max_length=255,blank=True)
    description = models.TextField(blank=True)
    thai_description = models.TextField(blank=True)
    units = models.IntegerField()    
    available_in_first_semester = models.BooleanField(default=True)
    available_in_second_semester = models.BooleanField(default=True)
    available_in_summer_semester = models.BooleanField(default=True)
    years_available = models.IntegerField(default=1)
    
    institution = models.ForeignKey('Institution')
    prerequisites = models.ManyToManyField('Prerequisite', related_name='required_by_subjects', blank=True)
    
    def __unicode__(self):
        return unicode(self.code + ": " + self.name)
        
class Prerequisite(models.Model):
    """(Prerequisite description)"""
    # name = models.CharField(blank=True, max_length=255)
    is_parallelable = models.BooleanField(default=False) # can be register alongside required subject
    
    subjects = models.ManyToManyField('Subject', related_name='required_by_prerequisites')

    def __unicode__(self):
        identifier = {True: "Pararellable: ", False: "NOT Pararellable: "}
        return unicode(identifier[self.is_parallelable] + ", ".join([s.code for s in self.subjects.all()]))

        
class Group(models.Model): #กลุ่มวิชาบังคับเลือก
    """(Group description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    required_units = models.IntegerField()
    
    institution = models.ForeignKey('Institution')
    subjects = models.ManyToManyField('Subject')

    def __unicode__(self):
        return unicode(self.name)
        
class Field(models.Model): #สายวิชา
    """(Field description)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    institution = models.ForeignKey('Institution')
    course = models.ForeignKey('Course')
    subjects = models.ManyToManyField('Subject')

    def __unicode__(self):
        return unicode(self.name)
#
# User Profile
#    
class UserProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)
    
    YEAR_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
    )
    SEMESTER_CHOICES = (
        (1, 'First'),
        (2, 'Second'),
        (3, 'Summer'),
    )
    
    year = models.IntegerField(choices=YEAR_CHOICES, default=1)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)

    institution = models.ForeignKey('Institution')
    course = models.ForeignKey('Course')
    # subjects = models.ManyToManyField('Subject')
    
    def __unicode__(self):
        return unicode(self.user.username)

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        # fields = ['institution', 'course']

    
