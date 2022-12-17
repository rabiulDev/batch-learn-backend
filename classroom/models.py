import uuid
from django.db import models
from student.models import StudentProfile
from teacher.models import TeacherProfile, Subject
from school.models import School


# Create your models here.
# class_total_amount = models.DecimalField(max_digits=5, decimal_places=1)
# lesson_space_room_id = null,
class Classroom(models.Model):

    CLASSROOM_STATUS = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Expired', 'Expired'),
    ]

    teacher = models.ForeignKey(TeacherProfile, null=True, blank=True, on_delete=models.SET_NULL)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    classroom_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=20, null=True, blank=True, default='Pending', choices=CLASSROOM_STATUS),
    class_date = models.DateTimeField()
    is_free_class = models.BooleanField(default=False)
    class_started_at = models.DateTimeField(null=True, blank=True)
    class_ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(StudentProfile, through='ClassroomStudent')
    creator = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True, related_name='creator')


class ClassroomStudent(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('classroom', 'student',)

