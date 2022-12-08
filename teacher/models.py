from django.db import models
from django.contrib.auth.models import User

from school.models import School


# Create your models here.
class TeacherType(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ClassTool(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=18)
    teacher_type = models.ForeignKey(TeacherType, on_delete=models.PROTECT)
    subjects = models.ManyToManyField(Subject)
    serve_or_attend_school = models.ManyToManyField(School)
    classes_tools = models.ManyToManyField(ClassTool)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.email


