# Generated by Django 5.0 on 2024-02-21 09:14

import sounds.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0002_soundtone_duration_rec'),
    ]

    operations = [
        migrations.AddField(
            model_name='soundsource',
            name='midi_vel_preferred',
            field=models.PositiveSmallIntegerField(blank=True, choices=sounds.models.choice_midi_value, default=None, help_text='The preferred MIDI velocity', null=True),
        ),
        migrations.AlterField(
            model_name='soundtone',
            name='category',
            field=models.CharField(blank=True, choices=[('unknown', 'Unknown'), ('bass', 'Bass'), ('pad', 'Pad'), ('lead', 'Lead'), ('piano', 'Piano'), ('keyboard', 'Keyboard'), ('strings', 'Strings'), ('ensemble', 'Ensemble'), ('woodwind', 'Woodwind'), ('brass', 'Brass'), ('synth', 'Synth'), ('drone', 'Drone'), ('drum', 'Drum'), ('percussion', 'Percussion'), ('pluck', 'Pluck'), ('guitar', 'Guitar'), ('rythm', 'Rythm'), ('loop', 'Loop'), ('sample', 'Sample'), ('song', 'Song'), ('soundfx', 'Sound FX'), ('vocal', 'Vocal'), ('vocoder', 'Vocoder'), ('voice', 'Voice'), ('baritone', 'Baritone'), ('alto', 'Alto'), ('soprano', 'Soprano'), ('spoken', 'Spoken')], default=None, help_text='Category of sound', max_length=16, null=True),
        ),
    ]
