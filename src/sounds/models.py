from django.db import models
from django.db.models.signals import pre_save
from tags.models import Tag
import json_normalize

def default_channels():
    return [1,2]


class SoundGenerator(models.Model):

    class Type(models.TextChoices):
        RECORDING  = 'recording'
        INSTRUMENT = 'instrument'
        ARTIST     = 'artist'

    
    id          = models.AutoField(primary_key=True) 
    # type and descriptions
    type        = models.CharField(max_length=16,choices=Type.choices,default=Type.INSTRUMENT,help_text="Type of generator")
    name        = models.CharField(max_length=64,null=False,help_text="The name of the sound generator")
    description = models.TextField(max_length=256,null=True,default=None)
    filenames   = models.TextField(max_length=256,null=True,default=None,help_text="The list of possible file names for the plugin")
    file_path   = models.FilePathField(max_length=512,null=True,default=None,help_text="File path for the plugin")
    # capture/control audio/midi parameters
    audio_device_name = models.CharField(max_length=64,default=None,null=True,help_text="Audio input device")
    audio_device_channels = models.JSONField(default=default_channels,null=True,help_text="Audio input channels")
    audio_device_samplerate = models.PositiveSmallIntegerField(default=44100,help_text="Audio input sample rate")
    audio_device_kernelsize = models.PositiveSmallIntegerField(default=256,help_text="Audio input kernel size")
    audio_device_sample_format = models.SmallIntegerField(default=16,help_text="Audio input resolution")
    midi_out_port_name = models.CharField(max_length=64,default=None,null=True,help_text="MIDI OUT port name")
    midi_in_port_name = models.CharField(max_length=64,default=None,null=True,help_text="MIDI IN port name")
    midi_channel = models.PositiveSmallIntegerField(default=None,null=True,help_text="MIDI channel")    
    # extra parameters
    parameters  = models.JSONField(default=None,null=True,help_text="Extra Parameters for this generator")

    class Meta:
        indexes = [
#            models.Index(fields=['name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"],name="generator_name_unique")
        ]

class SoundProcessor(models.Model):
    id          = models.AutoField(primary_key=True) 
    name        = models.CharField(max_length=64,null=False,help_text="The name of the sound processor")
    description = models.TextField(max_length=256,null=True,default=None)
    filenames   = models.TextField(max_length=256,null=True,default=None,help_text="The list of possible file names for the plugin")

    class Meta:
        indexes = [
#            models.Index(fields=['name']),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"],name="processor_name_unique")
        ]        


class SoundSource(models.Model):

    class Type(models.TextChoices):
        UNKNOWN    = 'unknown'
        VOICE      = 'voice'
        INSTRUMENT = 'instrument'
        EFFECT     = 'effect'
        SOUND_FX   = 'soundfx'

    class Nature(models.TextChoices):
        UNKNOWN    = 'unknown'
        NATURAL    = 'natural'
        ACCOUSTIC  = 'accoustic'
        ELECTRIC   = 'electric'
        ELEC_ACC   = 'elec_acc'
        ELECTRONIC = 'electronic'
        ANALOG     = 'analog'
        DIGITAL    = 'digital'
        NEURAL     = 'neural'

    class Category(models.TextChoices):
        UNKNOWN = 'unknown'
        VOICE = 'voice'
        BASS = 'bass'
        LEAD = 'lead'
        PIANO = 'piano'
        KEYBOARD = 'keyboard'
        STRING = 'string'
        ENSEMBLE = 'ensemble'
        WIND = 'wind'
        BRASS = 'brass'
        SYNTH = 'synth'
        DRONE = 'drone'
        DRUM = 'drum'
        PERCUSSION = 'percussion'
        GUITAR = 'guitar'
        SOUND_FX = 'soundfx'

    @staticmethod
    def normalize_parameters(instance):
        if instance.tag is None:
            return
        instance.parameters = json_normalize(instance.parameters)

    @staticmethod
    def pre_save(sender, instance, **kwargs):
        SoundSource.normalize_parameters(instance)

    id            = models.AutoField(primary_key=True) 
    generator     = models.ForeignKey(SoundGenerator,default=None,null=True,on_delete=models.CASCADE)
    type          = models.CharField(max_length=16,choices=Type.choices,default=Type.UNKNOWN,help_text="Type of sound")
    nature        = models.CharField(max_length=16,choices=Nature.choices,default=Nature.UNKNOWN,help_text="The Nature of the sound")
    category      = models.CharField(max_length=16,choices=Category.choices,default=Category.UNKNOWN,help_text="Category of sound")
    parameters    = models.JSONField(help_text="Parameters for this specific sound") # can be text pronounced by the vocal artist 
    recording     = models.FilePathField(max_length=512,null=True,default=None,help_text="File path for recorded sources")
    last_modified = models.DateTimeField(default=None,null=True,help_text="the date/time the file was modified")
    record_date   = models.DateTimeField(auto_now_add=True,help_text="the date/time the file was entered in the database")
    # relations
    tags          = models.ManyToManyField(Tag,related_name="sounds")

    class Meta:
        ordering = ['record_date']
        indexes = [
            models.Index(fields=['record_date']),
            models.Index(fields=['generator']),
            models.Index(fields=['type']),
            models.Index(fields=['nature']),
        ]
        constraints = [
            models.UniqueConstraint(fields=["recording"],name="recording_is_unique"),
            models.UniqueConstraint(fields=["generator","parameters"],name="generator_parameters_is_unique"),
        ]

pre_save.connect(SoundSource.pre_save, SoundSource)        


class SoundBite(models.Model):

    id            = models.AutoField(primary_key=True) 
    source        = models.ForeignKey(SoundSource,null=False,on_delete=models.CASCADE)
    processor     = models.ForeignKey(SoundProcessor,default=None,null=True,on_delete=models.CASCADE)
    # format = { "source : { ...params... } , processors: [ { ...params... } ]"}
    parameters    = models.JSONField(help_text="Parameters for this specific soundbite (generator(if+processor parameters)")
    file_path     = models.FilePathField(max_length=512,null=False,help_text="File path of the waveform")
    last_modified = models.DateTimeField(default=None,null=True,help_text="the date/time the file was modified")
    record_date   = models.DateTimeField(auto_now_add=True,help_text="the date/time the file was entered in the database")

    class Meta:
        ordering = ['record_date']
        indexes = [
            models.Index(fields=['record_date']),
            models.Index(fields=['file_path']),
        ]
        constraints = [
#            models.UniqueConstraint(fields=["doc_id", "vector_store"],name="doc_id_vector_store_unique")
#            models.UniqueConstraint(fields=["application","file_path"],name="application_file_path_unique")
        ]    
    