# Generated by Django 5.0 on 2024-05-28 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0015_remove_soundsource_preset_extra_delay_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soundsource',
            name='preset_delay_factor',
        ),
    ]
