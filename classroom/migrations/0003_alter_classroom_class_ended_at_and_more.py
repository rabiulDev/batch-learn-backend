# Generated by Django 4.1.3 on 2022-12-17 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_alter_classroom_class_ended_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='class_ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='class_started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
