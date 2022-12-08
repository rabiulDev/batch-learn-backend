from django.contrib import admin
from .models import TeacherProfile, Subject, TeacherType, ClassTool

# Register your models here.
admin.site.register(ClassTool)
admin.site.register(Subject)
admin.site.register(TeacherType)
admin.site.register(TeacherProfile)



