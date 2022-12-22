# Generated by Django 4.1.3 on 2022-12-22 06:51

from django.db import migrations, models
import student.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_alter_studentprofile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=student.models.upload_to, verbose_name='Avatar'),
        ),
    ]