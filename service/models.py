from django.db import models

# Create your models here.
class User(models.Model):
    openId=models.CharField(max_length=255,null=True)
    identity=models.BigIntegerField(null=True)
    name=models.CharField(max_length=255,null=True)
    number=models.CharField(max_length=255,null=True)
    faceUrl=models.CharField(max_length=255,null=True)

class Course(models.Model):
    courseId=models.CharField(max_length=255,null=True)
    courseName=models.CharField(max_length=255,null=True)
    endTime=models.DateTimeField (null=True)
    # state=models.BooleanField ()

class CourseForUser(models.Model):
    courseId=models.CharField(max_length=255,null=True)
    number=models.CharField(max_length=255,null=True)

class SignInForTeacher(models.Model):
    courseId=models.CharField(max_length=255,null=True)
    number=models.CharField(max_length=255,null=True)
    section=models.BigIntegerField(null=True)
    startTime=models.DateTimeField (null=True)
    endTime=models.DateTimeField (null=True)
    longitude=models.FloatField (null=True)
    latitude=models.FloatField (null=True)

class SignInForStudent(models.Model):
    courseId=models.CharField(max_length=255,null=True)
    number=models.CharField(max_length=255,null=True)
    section=models.BigIntegerField(null=True)
    time=models.DateTimeField (null=True)
    longitude=models.FloatField (null=True)
    latitude=models.FloatField (null=True)

class SupSignIn(models.Model):
    courseId=models.CharField(max_length=255,null=True)
    number=models.CharField(max_length=255,null=True)
    section=models.BigIntegerField(null=True)
    time=models.DateTimeField (null=True)
    reason=models.CharField(max_length=255,null=True)
    state=models.BooleanField ()
