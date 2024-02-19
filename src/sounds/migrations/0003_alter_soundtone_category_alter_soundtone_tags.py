# Generated by Django 5.0 on 2024-02-19 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0002_remove_soundsource_generator_name_unique_and_more'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soundtone',
            name='category',
            field=models.CharField(blank=True, choices=[('unknown', 'Unknown'), ('bass', 'Bass'), ('pad', 'Pad'), ('lead', 'Lead'), ('piano', 'Piano'), ('keyboard', 'Keyboard'), ('strings', 'Strings'), ('ensemble', 'Ensemble'), ('woodwind', 'Woodwind'), ('brass', 'Brass'), ('synth', 'Synth'), ('drone', 'Drone'), ('drum', 'Drum'), ('percussion', 'Percussion'), ('pluck', 'Pluck'), ('guitar', 'Guitar'), ('rythm', 'Rythm'), ('sample', 'Sample'), ('song', 'Song'), ('soundfx', 'Sound Fx'), ('voice', 'Voice'), ('baritone', 'Baritone'), ('alto', 'Alto'), ('soprano', 'Soprano'), ('spoken', 'Spoken')], default=None, help_text='Category of sound', max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='soundtone',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='sounds', to='tags.tag'),
        ),
    ]