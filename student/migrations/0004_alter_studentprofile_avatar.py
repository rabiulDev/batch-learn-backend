# Generated by Django 4.1.3 on 2022-12-21 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_studentprofile_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='Null', upload_to='avatars'),
        ),
    ]
