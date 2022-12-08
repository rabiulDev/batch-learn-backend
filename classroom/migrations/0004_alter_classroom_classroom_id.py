# Generated by Django 4.1.3 on 2022-12-05 12:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_remove_classroom_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='classroom_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
