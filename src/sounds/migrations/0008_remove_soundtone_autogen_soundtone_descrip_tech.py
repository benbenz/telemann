# Generated by Django 5.0 on 2024-02-21 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0007_soundtone_autogen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soundtone',
            name='autogen',
        ),
        migrations.AddField(
            model_name='soundtone',
            name='descrip_tech',
            field=models.TextField(blank=True, default=None, help_text='Technical description automatically generated by the system', max_length=512, null=True),
        ),
    ]
