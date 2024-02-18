# Generated by Django 5.0 on 2024-02-18 19:52

import django.db.models.deletion
import sounds.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoundBite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file_path', models.FilePathField(help_text='File path of the waveform', max_length=512)),
                ('notes', models.JSONField(blank=True, default=None, help_text='The notes played', null=True)),
                ('duration_gen', models.FloatField(blank=True, default=None, help_text='The duration of generation the sound', null=True)),
                ('duration_snd', models.FloatField(blank=True, default=None, help_text='The actual duration of the sound', null=True)),
                ('parameters', models.JSONField(blank=True, default=None, help_text='Parameters for this specific soundbite (generator(if+processor parameters)', null=True)),
                ('last_modified', models.DateTimeField(default=None, help_text='the date/time the file was modified', null=True)),
                ('record_date', models.DateTimeField(auto_now_add=True, help_text='the date/time the file was entered in the database')),
            ],
            options={
                'ordering': ['record_date'],
            },
        ),
        migrations.CreateModel(
            name='SoundDataset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The name of the sound dataset', max_length=64)),
                ('description', models.CharField(default=None, help_text='A short description', max_length=256, null=True)),
                ('last_modified', models.DateTimeField(default=None, help_text='the date/time the file was modified', null=True)),
                ('record_date', models.DateTimeField(auto_now_add=True, help_text='the date/time the file was entered in the database')),
            ],
            options={
                'ordering': ['record_date'],
            },
        ),
        migrations.CreateModel(
            name='SoundGenerator',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('recording', 'Recording'), ('instrument', 'Instrument'), ('voice', 'Voice')], default='instrument', help_text='Type of generator', max_length=16)),
                ('nature', models.CharField(choices=[('unknown', 'Unknown'), ('natural', 'Natural'), ('accoustic', 'Accoustic'), ('electric', 'Electric'), ('elec_acc', 'Elec Acc'), ('electronic', 'Electronic'), ('digital', 'Digital'), ('sample', 'Sample')], default='unknown', help_text='The Nature of the sound', max_length=16)),
                ('synthesis', models.CharField(choices=[('unknown', 'Unknown'), ('natural', 'Natural'), ('analog', 'Analog'), ('virtual_analog', 'Virtual Analog'), ('digital', 'Digital'), ('neural', 'Neural'), ('granular', 'Granular'), ('fm', 'Fm'), ('sampling', 'Sampling'), ('hybrid', 'Hybrid')], default='unknown', help_text='The Synthesis type of the sound', max_length=16)),
                ('name', models.CharField(help_text="The name of the sound generator: 'SynthMaster', 'Diva', etc.", max_length=64)),
                ('description', models.CharField(default=None, help_text='A short description', max_length=256, null=True)),
                ('audio_device_name', models.CharField(blank=True, default=None, help_text='Audio input device', max_length=64, null=True)),
                ('audio_device_samplerate', models.PositiveSmallIntegerField(choices=[(16000, '16kHz'), (22050, '22kHz'), (32000, '32kHz'), (44100, '44.1kHz'), (48000, '48kHz'), (96000, '96kHz')], default=44100, help_text='Audio input sample rate')),
                ('audio_device_channels', models.CharField(blank=True, choices=[('1', 'Mono 1'), ('2', 'Mono 2'), ('3', 'Mono 3'), ('4', 'Mono 4'), ('5', 'Mono 5'), ('6', 'Mono 6'), ('7', 'Mono 7'), ('8', 'Mono 8'), ('9', 'Mono 9'), ('10', 'Mono 10'), ('11', 'Mono 11'), ('12', 'Mono 12'), ('13', 'Mono 13'), ('14', 'Mono 14'), ('15', 'Mono 15'), ('16', 'Mono 16'), ('1,2', 'Stereo 1/2'), ('3,4', 'Stereo 3/4'), ('5,6', 'Stereo 5/6'), ('7,8', 'Stereo 7/8'), ('9,10', 'Stereo 9/10'), ('11,12', 'Stereo 11/12'), ('13,14', 'Stereo 13/4'), ('15,16', 'Stereo 15/16')], default=None, help_text='Audio input channels', max_length=5, null=True)),
                ('audio_device_kernelsize', models.PositiveSmallIntegerField(blank=True, choices=[(64, '64'), (128, '128'), (256, '256'), (512, '512'), (1024, '1024')], default=None, help_text='Audio input kernel size', null=True)),
                ('audio_device_sample_format', models.SmallIntegerField(blank=True, choices=[(16, '16 bits'), (24, '24 bits'), (32, '32 bits')], default=None, help_text='Audio input resolution', null=True)),
                ('midi_out_port_name', models.CharField(blank=True, default=None, help_text='MIDI OUT port name', max_length=64, null=True)),
                ('midi_in_port_name', models.CharField(blank=True, default=None, help_text='MIDI IN port name', max_length=64, null=True)),
                ('midi_channel', models.PositiveSmallIntegerField(blank=True, choices=[(0, '1'), (1, '2'), (2, '3'), (3, '4'), (4, '5'), (5, '6'), (6, '7'), (7, '8'), (8, '9'), (9, '10'), (10, '11'), (11, '12'), (12, '13'), (13, '14'), (14, '15'), (15, '16')], default=None, help_text='MIDI channel', null=True)),
                ('filenames', models.CharField(blank=True, default=None, help_text='Optional: the list of possible file names for the plugin (comma separated)', max_length=256, null=True)),
                ('file_path', models.FilePathField(default=None, help_text='Optional: the file path for the plugin (requried if this is a plugin)', max_length=512, null=True)),
                ('parameters', models.JSONField(blank=True, default=None, help_text='Extra Parameters for this generator', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SoundProcessor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The name of the sound processor', max_length=64)),
                ('description', models.TextField(default=None, max_length=256, null=True)),
                ('filenames', models.TextField(default=None, help_text='The list of possible file names for the plugin', max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SoundSource',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('unknown', 'Unknown'), ('voice', 'Voice'), ('sound', 'Sound'), ('instrument', 'Instrument'), ('effect', 'Effect'), ('soundfx', 'Sound Fx')], default='unknown', help_text='Type of sound', max_length=16)),
                ('category', models.CharField(choices=[('unknown', 'Unknown'), ('bass', 'Bass'), ('lead', 'Lead'), ('piano', 'Piano'), ('keyboard', 'Keyboard'), ('string', 'String'), ('ensemble', 'Ensemble'), ('wind', 'Wind'), ('brass', 'Brass'), ('synth', 'Synth'), ('drone', 'Drone'), ('drum', 'Drum'), ('percussion', 'Percussion'), ('guitar', 'Guitar'), ('guitar_folk', 'Guitar Folk'), ('guitar_elec', 'Guitar Electric'), ('guitar_classic', 'Guitar Classic'), ('rythm', 'Rythm'), ('sample', 'Sample'), ('soundfx', 'Sound Fx'), ('voice', 'Voice'), ('baritone', 'Baritone'), ('alto', 'Alto'), ('soprano', 'Soprano')], default='unknown', help_text='Category of sound', max_length=16)),
                ('parameters', models.JSONField(blank=True, default=None, help_text='Parameters for this specific sound', null=True)),
                ('midi_bank', models.SmallIntegerField(blank=True, choices=sounds.models.choice_midi_bank, default=None, help_text='The MIDI bank of the sound', null=True)),
                ('midi_program', models.SmallIntegerField(blank=True, choices=sounds.models.choice_midi_program, default=None, help_text='The MIDI program of the sound', null=True)),
                ('recording', models.FilePathField(default=None, help_text='File path for recorded sources', max_length=512, null=True)),
                ('last_modified', models.DateTimeField(default=None, help_text='the date/time the file was modified', null=True)),
                ('record_date', models.DateTimeField(auto_now_add=True, help_text='the date/time the file was entered in the database')),
            ],
            options={
                'ordering': ['record_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='sounddataset',
            constraint=models.UniqueConstraint(fields=('name',), name='sounddataset_name_is_unique'),
        ),
        migrations.AddField(
            model_name='soundbite',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sounds.sounddataset'),
        ),
        migrations.AddIndex(
            model_name='soundgenerator',
            index=models.Index(fields=['nature'], name='sounds_soun_nature_c1fe44_idx'),
        ),
        migrations.AddConstraint(
            model_name='soundgenerator',
            constraint=models.UniqueConstraint(fields=('name',), name='generator_name_unique'),
        ),
        migrations.AddConstraint(
            model_name='soundprocessor',
            constraint=models.UniqueConstraint(fields=('name',), name='processor_name_unique'),
        ),
        migrations.AddField(
            model_name='soundbite',
            name='processor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='sounds.soundprocessor'),
        ),
        migrations.AddField(
            model_name='soundsource',
            name='generator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sounds.soundgenerator'),
        ),
        migrations.AddField(
            model_name='soundsource',
            name='tags',
            field=models.ManyToManyField(related_name='sounds', to='tags.tag'),
        ),
        migrations.AddField(
            model_name='soundbite',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sounds.soundsource'),
        ),
        migrations.AddIndex(
            model_name='soundsource',
            index=models.Index(fields=['record_date'], name='sounds_soun_record__475bc9_idx'),
        ),
        migrations.AddIndex(
            model_name='soundsource',
            index=models.Index(fields=['generator'], name='sounds_soun_generat_d9ca2b_idx'),
        ),
        migrations.AddIndex(
            model_name='soundsource',
            index=models.Index(fields=['type'], name='sounds_soun_type_d5a17c_idx'),
        ),
        migrations.AddConstraint(
            model_name='soundsource',
            constraint=models.UniqueConstraint(fields=('recording',), name='recording_is_unique'),
        ),
        migrations.AddConstraint(
            model_name='soundsource',
            constraint=models.UniqueConstraint(fields=('generator', 'midi_bank', 'midi_program'), name='generator_bank_program_is_unique'),
        ),
        migrations.AddIndex(
            model_name='soundbite',
            index=models.Index(fields=['record_date'], name='sounds_soun_record__7bf484_idx'),
        ),
        migrations.AddIndex(
            model_name='soundbite',
            index=models.Index(fields=['file_path'], name='sounds_soun_file_pa_123c0c_idx'),
        ),
    ]
