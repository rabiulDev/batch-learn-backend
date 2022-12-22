from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from school.models import School


# Create your models here.
def upload_to(instance, filename):
    return 'avatars/{filename}'.format(filename=filename)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    is_lead = models.BooleanField(default=False)
    avatar = models.ImageField(_('Avatar'), upload_to=upload_to, blank=True)
    is_accept = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=18)
    coupon = models.CharField(max_length=20, null=True, blank=True)
