# Generated by Django 4.1.3 on 2022-12-25 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_studentprofile_avatar'),
        ('classroom', '0010_classroomstudentattachments_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroomstudentattachments',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_info', to='student.studentprofile'),
        ),
    ]
