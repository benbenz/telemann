from django.db import models
from django.db.models.signals import pre_save
from tags.models import Tag
import json_normalize

class SamplingFrequency(models.IntegerChoices):
    fs16000 = 16000 , ('16kHz')
    fs22050 = 22050 , ('22kHz')
    fs32000 = 32000 , ('32kHz')
    fs44100 = 44100 , ('44.1kHz')
    fs48000 = 48000 , ('48kHz')
    fs96000 = 96000 , ('96kHz')

class BufferSize(models.IntegerChoices):
    buf64 = 64 , ('64')
    buf128 = 128 , ('128')
    buf256 = 256 , ('256')
    buf512 = 512 , ('512')
    buf1024 = 1024 , ('1024')

class Resolution(models.IntegerChoices):
    res16 = 16 , ('16 bits')
    res24 = 24 , ('24 bits')
    res32 = 32 , ('32 bits')

class MIDIChannel(models.IntegerChoices):
    ch1 = 0 , ('1')
    ch2 = 1 , ('2')
    ch3 = 2 , ('3')
    ch4 = 3 , ('4')
    ch5 = 4 , ('5')
    ch6 = 5 , ('6')
    ch7 = 6 , ('7')
    ch8 = 7 , ('8')
    ch9 = 8 , ('9')
    ch10 = 9 , ('10')
    ch11 = 10 , ('11')
    ch12 = 11 , ('12')
    ch13 = 12 , ('13')
    ch14 = 13 , ('14')
    ch15 = 14 , ('15')
    ch16 = 15 , ('16')


class AudioIO(models.TextChoices):
    mono1 = "1" , 'Mono 1'
    mono2 = "2" , 'Mono 2'
    mono3 = "3" , 'Mono 3'
    mono4 = "4" , 'Mono 4'
    mono5 = "5" , 'Mono 5'
    mono6 = "6" , 'Mono 6'
    mono7 = "7" , 'Mono 7'
    mono8 = "8" , 'Mono 8'
    mono9 = "9" , 'Mono 9'
    mono10 = "10" , 'Mono 10'
    mono11 = "11" , 'Mono 11'
    mono12 = "12" , 'Mono 12'
    mono13 = "13" , 'Mono 13'
    mono14 = "14" , 'Mono 14'
    mono15 = "15" , 'Mono 15'
    mono16 = "16" , 'Mono 16'
    stereo1_2 = "1,2" , 'Stereo 1/2'
    stereo3_4 = "3,4" , 'Stereo 3/4'
    stereo5_6 = "5,6" , 'Stereo 5/6'
    stereo7_8 = "7,8" , 'Stereo 7/8'
    stereo9_10 = "9,10" , 'Stereo 9/10'
    stereo11_12 = "11,12" , 'Stereo 11/12'
    stereo13_14 = "13,14" , 'Stereo 13/4'
    stereo15_16 = "15,16" , 'Stereo 15/16'

class SoundGenerator(models.Model):

    class Type(models.TextChoices):
        AUDIOFILES  = 'files'
        RECORDING   = 'recording'
        INSTRUMENT  = 'instrument'
        ARTIST      = 'artist'
    
    id          = models.AutoField(primary_key=True) 
    # type and descriptions
    type        = models.CharField(max_length=16,choices=Type.choices,default=Type.INSTRUMENT,help_text="Type of generator")
    name        = models.CharField(max_length=64,null=False,help_text="The name of the sound generator: 'SynthMaster', 'Diva', etc.")
    description = models.CharField(max_length=256,null=True,default=None,help_text="A short description")
    # capture/control audio/midi parameters
    audio_device_name = models.CharField(max_length=64,default=None,null=True,blank=True,help_text="Audio input device")
    audio_device_samplerate = models.PositiveSmallIntegerField(default=SamplingFrequency.fs44100,choices=SamplingFrequency.choices,help_text="Audio input sample rate")
    audio_device_channels = models.CharField(max_length=5,default=None,choices=AudioIO.choices,null=True,blank=True,help_text="Audio input channels")
    audio_device_kernelsize = models.PositiveSmallIntegerField(default=None,choices=BufferSize.choices,null=True,blank=True,help_text="Audio input kernel size")
    audio_device_sample_format = models.SmallIntegerField(default=None,choices=Resolution.choices,null=True,blank=True,help_text="Audio input resolution")
    midi_out_port_name = models.CharField(max_length=64,default=None,null=True,blank=True,help_text="MIDI OUT port name")
    midi_in_port_name = models.CharField(max_length=64,default=None,null=True,blank=True,help_text="MIDI IN port name")
    midi_channel = models.PositiveSmallIntegerField(default=None,null=True,blank=True,choices=MIDIChannel.choices,help_text="MIDI channel")    
    # audio plugin stuff
    filenames   = models.CharField(max_length=256,null=True,blank=True,default=None,help_text="Optional: the list of possible file names for the plugin (comma separated)")
    file_path   = models.FilePathField(max_length=512,null=True,default=None,help_text="Optional: the file path for the plugin (requried if this is a plugin)")
    # extra parameters
    parameters  = models.JSONField(default=None,null=True,blank=True,help_text="Extra Parameters for this generator")

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

class SoundDataSet(models.Model):
    
    id            = models.AutoField(primary_key=True) 
    name          = models.CharField(max_length=64,null=False,help_text="The name of the sound dataset")
    description   = models.CharField(max_length=256,null=True,default=None,help_text="A short description")
    last_modified = models.DateTimeField(default=None,null=True,help_text="the date/time the file was modified")
    record_date   = models.DateTimeField(auto_now_add=True,help_text="the date/time the file was entered in the database")

    class Meta:
        ordering = ['record_date']
        indexes = [
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"],name="sounddataset_name_is_unique"),
        ]


class Sound(models.Model):

    id            = models.AutoField(primary_key=True) 
    source        = models.ForeignKey(SoundSource,null=False,on_delete=models.CASCADE)
    processor     = models.ForeignKey(SoundProcessor,default=None,null=True,on_delete=models.CASCADE)
    # format = { "source : { ...params... } , processors: [ { ...params... } ]"}
    parameters    = models.JSONField(help_text="Parameters for this specific soundbite (generator(if+processor parameters)")
    file_path     = models.FilePathField(max_length=512,null=False,help_text="File path of the waveform")
    last_modified = models.DateTimeField(default=None,null=True,help_text="the date/time the file was modified")
    record_date   = models.DateTimeField(auto_now_add=True,help_text="the date/time the file was entered in the database")

    # relation
    dataset = models.ForeignKey(SoundDataSet,on_delete=models.CASCADE)

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
    

