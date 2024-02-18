# Generated by Django 5.0 on 2024-02-18 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soundgenerator',
            name='nature',
            field=models.CharField(choices=[('unknown', 'Unknown'), ('natural', 'Natural'), ('accoustic', 'Accoustic'), ('electric', 'Electric'), ('elec_acc', 'Elec Acc'), ('electronic', 'Electronic'), ('digital', 'Digital'), ('sample', 'Sample'), ('recording', 'Recording')], default='unknown', help_text='The Nature of the sound', max_length=16),
        ),
        migrations.AlterField(
            model_name='soundgenerator',
            name='synthesis',
            field=models.CharField(choices=[('unknown', 'Unknown'), ('natural', 'Natural'), ('accoustic', 'Accoustic'), ('electric', 'Electric'), ('elec_acc', 'Elec Acc'), ('analog', 'Analog'), ('digital', 'Digital'), ('virtual_analog', 'Virtual Analog'), ('neural', 'Neural'), ('granular', 'Granular'), ('fm', 'Fm'), ('sampling', 'Sampling'), ('hybrid', 'Hybrid')], default='unknown', help_text='The Synthesis type of the sound', max_length=16),
        ),
    ]
