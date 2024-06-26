# Generated by Django 5.0 on 2024-05-28 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0013_alter_dataset_last_modified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='soundsource',
            name='preset_extra_delay',
            field=models.PositiveSmallIntegerField(blank=True, default=None, help_text='the extra delay to apply to the preset change', null=True),
        ),
    ]
