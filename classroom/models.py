import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from school.models import School
from student.models import StudentProfile
from teacher.models import TeacherProfile, Subject


class Classroom(models.Model):
    CLASSROOM_STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('started', 'Started'),
        ('ended', 'Ended'),
        ('expired', 'Expired'),
    ]

    teacher = models.ForeignKey(TeacherProfile, null=True, blank=True, on_delete=models.SET_NULL)
    school = models.ForeignKey(School, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    classroom_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=CLASSROOM_STATUS, default='Pending')
    class_date = models.DateTimeField()
    is_free_class = models.BooleanField(default=False)
    class_started_at = models.DateTimeField(null=True, blank=True)
    class_ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(StudentProfile, through='ClassroomStudent')
    creator = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True, related_name='creator')

    def __str__(self):
        return str(self.classroom_id)

    def accept_teacher(self, user):
        current_date = timezone.now()
        if self.class_date > current_date:
            try:
                teacher = TeacherProfile.objects.get(user=user)
                if self.teacher:
                    return 'This class is already accepted by another teacher'
                elif not self.teacher:
                    self.teacher = teacher
                    self.status = 'Accepted'
                    self.save()
                    return 'True'
            except Exception:
                return 'You are not allowed for Teacher'
        else:
            return 'This class is expired'

    def start_class(self, user):
        current_date = timezone.now()
        try:
            teacher = TeacherProfile.objects.get(user=user)
            if teacher == self.teacher:
                if self.class_date > current_date:
                    return 'This is not the time to go live'
                elif self.status == 'Started' and self.class_started_at:
                    return 'This class is already live'
                elif not self.class_started_at and self.class_date <= current_date:
                    self.class_started_at = current_date
                    self.status = 'Started'
                    self.save()
                    return 'Start'
                return 'This class is already expired or ended'
            return 'You have no access to live this class'
        except Exception:
            return "You are not a teacher"

    def end_class(self, user):
        current_date = timezone.now()
        try:
            teacher = TeacherProfile.objects.get(user=user)
            if teacher == self.teacher:
                if not self.class_ended_at and self.status == 'Started':
                    self.class_ended_at = current_date
                    self.status = 'Ended'
                    self.save()
                    return 'End'
                elif self.status == 'Ended' and self.class_ended_at:
                    return 'This class is already ended'
                return 'This class is not started yet'
            return 'You have no access to end this class'
        except Exception:
            return "You are not a teacher"

    def has_profile(self, user_id):
        if self.teacher is not None:
            try:
                if self.teacher == TeacherProfile.objects.get(user_id=user_id):
                    return True
            except TeacherProfile.DoesNotExist:
                pass
        return bool(self.students.filter(user_id=user_id).exists())

    def check_student(self, user_id):
        try:
            if StudentProfile.objects.get(user_id=user_id) in self.students.all():
                return True
        except StudentProfile.DoesNotExist:
            return False

    def check_teacher(self, user_id):
        if self.teacher is not None:
            try:
                if self.teacher == TeacherProfile.objects.get(user_id=user_id):
                    return True
            except TeacherProfile.DoesNotExist:
                pass
        return False

class ClassroomStudent(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('classroom', 'student',)


class ClassRoomComments(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def get_profile_avatar(self):
        group_list = [group.name for group in self.creator.groups.all()]
        if 'Student' in group_list:
            return StudentProfile.objects.get(user=self.creator).avatar
        elif 'Teacher' in group_list:
            return TeacherProfile.objects.get(user=self.creator).avatar
        return None


class ClassRoomReplyComments(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(ClassRoomComments, on_delete=models.CASCADE, related_name='reply_comments')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_profile_avatar(self):
        group_list = [group.name for group in self.creator.groups.all()]
        if 'Student' in group_list:
            return StudentProfile.objects.get(user=self.creator).avatar
        elif 'Teacher' in group_list:
            return TeacherProfile.objects.get(user=self.creator).avatar
        return None

def upload_to(instance, filename):
    return 'attachment/{filename}'.format(filename=filename)


class ClassRoomStudentAttachments(models.Model):
    file = models.ImageField(_('Attachment'), upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='student_info')


class ClassRoomTeacherAttachments(models.Model):
    file = models.ImageField(_('Attachment'), upload_to=upload_to)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
