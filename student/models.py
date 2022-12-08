from django.db import models
from django.contrib.auth.models import User

from school.models import School


# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    is_lead = models.BooleanField(default=False)
    is_accept = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=18)
    coupon = models.CharField(max_length=20, null=True, blank=True)


