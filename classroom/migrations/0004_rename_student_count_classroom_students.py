# Generated by Django 4.1.3 on 2022-12-17 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_alter_classroom_class_ended_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classroom',
            old_name='student_count',
            new_name='students',
        ),
    ]