# Generated by Django 4.1.3 on 2022-12-23 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0006_classroomcomments_alter_classroom_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroomreplycomments',
            name='parent_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_comments', to='classroom.classroomcomments'),
        ),
    ]
