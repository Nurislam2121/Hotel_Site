# Generated by Django 5.1.3 on 2025-05-13 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_remove_room_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
