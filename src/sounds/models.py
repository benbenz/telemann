from django.db import models
from django.db.models.signals import pre_save
from tags.models import Tag
from json_normalize import json_normalize
import json
from .core.defs import MIDIRange

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

def choice_midi_program():
    list = []
    for i in range(128):
        list.append( (i,i) )
    return list

def choice_midi_bank():
    list = []
    for i in range(128): #MSB x LSB
        list.append( (i,i) )
    return list

def choice_midi_value():
    list = []
    for i in range(128): #MSB x LSB
        list.append( (i,i) )
    return list

def choice_midi_range():
    return tuple((i.value[0], i.value[1]) for i in MIDIRange)

class SoundSource(models.Model):

    class Type(models.TextChoices):
        FILES       = 'files'      # pre-recorded audio
        RECORDING   = 'recording'  # audio to be recorded (generic)
        VOICE       = 'voice'      # audio recorded using voice
        INSTRUMENT  = 'instrument' # audio recorded using an instrument

    class Nature(models.TextChoices):
        UNKNOWN    = 'unknown'
        NATURAL    = 'natural'
        ACCOUSTIC  = 'accoustic'
        ELECTRIC   = 'electric'
        ELEC_ACC   = 'elec_acc'
        ELECTRONIC = 'electronic'
        DIGITAL    = 'digital'
        RECORDING  = 'recording'

    class Synthesis(models.TextChoices):
        UNKNOWN  = 'unknown'
        PHYSICAL  = 'physical'
        ANALOG   = 'analog'
        DIGITAL  = 'digital'
        VIRTUAL_ANALOG = 'virtual_analog'
        SUBTRACTIVE = 'subtractive'
        ADDITIVE = 'additive'
        NEURAL   = 'neural'
        GRANULAR = 'granular'
        FM       = 'fm'
        SAMPLING = 'sampling'
        HYBRID   = 'hybrid'
    
    id          = models.AutoField(primary_key=True) 
    # type and descriptions
    type        = models.CharField(max_length=16,choices=Type.choices,default=Type.INSTRUMENT,help_text="Type of source")
    nature      = models.CharField(max_length=16,choices=Nature.choices,default=Nature.UNKNOWN,help_text="The Nature of the sound")
    synthesis   = models.CharField(max_length=16,choices=Synthesis.choices,default=Synthesis.UNKNOWN,help_text="The Synthesis type of the sound")
    name        = models.CharField(max_length=64,null=False,help_text="The name of the sound source: 'SynthMaster', 'Diva', etc.")
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
    midi_bank_num = models.IntegerField(choices=choice_midi_bank,null=True,default=None,blank=True,help_text="The MIDI bank maximum value")
    midi_bank_use_lsb = models.BooleanField(default=None,null=True,blank=True,help_text="If the Bank LSB is used or not")
    midi_velocity_pref = models.PositiveSmallIntegerField(default=None,choices=choice_midi_value,null=True,blank=True,help_text="The preferred MIDI velocity")
    # audio plugin stuff
    filenames   = models.CharField(max_length=256,null=True,blank=True,default=None,help_text="Optional: the list of possible file names for the plugin (comma separated)")
    file_path   = models.FilePathField(max_length=512,null=True,default=None,help_text="Optional: the file path for the plugin (requried if this is a plugin)")
    extension   = models.CharField(max_length=64,null=True,blank=True,default=None,help_text="Optional: the extension file for the synth, to parse the parameters and auto-generate text. Ex: synths.diva")
    # extra parameters
    parameters  = models.JSONField(default=None,null=True,blank=True,help_text="Extra Parameters for this source")

    class Meta:
        indexes = [
#            models.Index(fields=['name']),
            models.Index(fields=['nature']),
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"],name="source_name_unique")
        ]

    @staticmethod
    def normalize_parameters(instance):
        pass
        # if instance.parameters is None:
        #     return
        # json_normalized = json_normalize(instance.parameters)
        # instance.parameters = {k,v for k,v in json_normalized }

    @staticmethod
    def pre_save(sender, instance, **kwargs):
        SoundSource.normalize_parameters(instance)

pre_save.connect(SoundSource.pre_save, SoundSource)      



class Processor(models.Model):
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

class SoundTone(models.Model):

    class Category(models.TextChoices):
        # INSTRUMENTs categories
        UNKNOWN = 'unknown'
        BASS = 'bass'
        PAD = 'pad'
        LEAD = 'lead'
        PIANO = 'piano'
        KEYBOARD = 'keyboard'
        STRINGS = 'strings'
        ENSEMBLE = 'ensemble'
        WOODWIND = 'woodwind'
        BRASS = 'brass'
        SYNTH = 'synth'
        DRONE = 'drone'
        DRUM = 'drum'
        PERCUSSION = 'percussion'
        PLUCK = 'pluck'
        GUITAR = 'guitar'
        RYTHM = 'rythm'
        LOOP = 'loop'
        SAMPLE = 'sample'
        SONG = 'song'
        SOUND_FX = 'soundfx','Sound FX'
        SOUNDSCAPE = 'soundscape'
        VOCAL = 'vocal'
        VOCODER = 'vocoder'
        
        # VOICEs categories
        VOICE = 'voice'
        BARITONE = 'baritone'
        ALTO = 'alto'
        SOPRANO = 'soprano'
        SPOKEN = 'spoken'

    @staticmethod
    def normalize_parameters(instance):
        pass
        # if instance.parameters is None:
        #     return
        # instance.parameters = json_normalize(json.dumps(instance.parameters))

    @staticmethod
    def pre_save(sender, instance, **kwargs):
        SoundTone.normalize_parameters(instance)

    id            = models.AutoField(primary_key=True) 
    category      = models.CharField(max_length=16,choices=Category.choices,default=None,null=True,blank=True,help_text="Category of sound")
    name          = models.CharField(max_length=128,default=None,null=True,blank=True,help_text="The name of the sound tone")
    description   = models.TextField(max_length=512,null=True,default=None,blank=True,help_text="A short description for the sound texture, focussing on the timbre.")
    description_tech = models.TextField(max_length=512,null=True,default=None,blank=True,help_text="Technical description automatically generated by the system",verbose_name='Technical Description')
    rec_duration  = models.FloatField(null=True,default=None,blank=True,help_text="Recommended duration in seconds",verbose_name='Recommended Duration')
    rec_midi_range = models.PositiveSmallIntegerField(choices=choice_midi_range,null=True,default=None,blank=True,help_text="A recommended MIDI range for this sound",verbose_name='Recommended MIDI Range')
    parameters    = models.JSONField(default=None,null=True,blank=True,help_text="Parameters for this specific sound") # can be text pronounced by the vocal artist 
    midi_bank_msb = models.IntegerField(choices=choice_midi_bank,null=True,default=None,blank=True,help_text="The MIDI bank MSB of the sound")
    midi_bank_lsb = models.IntegerField(choices=choice_midi_bank,null=True,default=None,blank=True,help_text="The MIDI bank LSB of the sound")
    midi_program  = models.SmallIntegerField(choices=choice_midi_program,null=True,default=None,blank=True,help_text="The MIDI program of the sound")
    recording     = models.FilePathField(max_length=512,null=True,default=None,help_text="File path for recorded sources")
    last_modified = models.DateTimeField(auto_now=True,null=True,help_text="the date/time the file was modified")
    record_date   = models.DateTimeField(auto_now_add=True,help_text="the date/time the file was entered in the database")
    # relations
    source        = models.ForeignKey(SoundSource,default=None,null=False,on_delete=models.CASCADE)
    tags          = models.ManyToManyField(Tag,blank=True,related_name="sounds",help_text="Tags associated with the sound")

    class Meta:
        ordering = ['record_date']
        indexes = [
            models.Index(fields=['record_date']),
            models.Index(fields=['source']),
        ]
        constraints = [
            models.UniqueConstraint(fields=["recording"],name="recording_is_unique"),
            models.UniqueConstraint(fields=["source","midi_bank_msb","midi_bank_lsb","midi_program"],name="source_bank_program_is_unique"),
        ]

    def get_compatible_categories(self):
        if self.source is None:
            return sorted( SoundTone.Category.choices , key=lambda cat: cat[1] )
        voices_category = [
            SoundTone.Category.VOICE.value ,
            SoundTone.Category.BARITONE.value ,
            SoundTone.Category.ALTO.value ,
            SoundTone.Category.SOPRANO.value ,
            SoundTone.Category.SPOKEN.value ,
        ]
        if self.source.type == SoundSource.Type.INSTRUMENT:
            return sorted( filter( lambda x: x[0] not in voices_category,SoundTone.Category.choices) , key=lambda cat: cat[1])
        elif self.source.type == SoundSource.Type.VOICE:
            return sorted( filter( lambda x: x[0] in voices_category,SoundTone.Category.choices) , key=lambda cat: cat[1])
        else:
            return sorted( SoundTone.Category.choices , key=lambda cat: cat[1])

pre_save.connect(SoundTone.pre_save, SoundTone)      

class Dataset(models.Model):
    
    id            = models.AutoField(primary_key=True) 
    name          = models.CharField(max_length=64,null=False,help_text="The name of the sound dataset")
    description   = models.CharField(max_length=256,null=True,default=None,help_text="A short description")
    last_modified = models.DateTimeField(auto_now=True,null=True,help_text="the date/time the file was modified")
    record_date   = models.DateTimeField(auto_now_add=True,help_text="the date/time the file was entered in the database")

    class Meta:
        ordering = ['record_date']
        indexes = [
        ]
        constraints = [
            models.UniqueConstraint(fields=["name"],name="dataset_name_is_unique"),
        ]


class SoundBite(models.Model):

    id            = models.AutoField(primary_key=True) 
    file_path     = models.FilePathField(max_length=512,null=False,help_text="File path of the waveform")
    # the description_tech maybe randomized from the SoundTone so we save it for each SoundBite.
    # The 'description' field is not changing across SoundBites of the same SoundTone so we leave it stored in the SoundTone class
    description_tech = models.TextField(max_length=512,null=True,default=None,blank=True,help_text="Technical description automatically generated by the system for this soundbite",verbose_name='Technical Description')
    notes         = models.JSONField(null=True,default=None,blank=True,help_text="The notes played")
    duration_gen  = models.FloatField(null=True,default=None,blank=True,help_text="The duration of generation the sound")
    duration_snd  = models.FloatField(null=True,default=None,blank=True,help_text="The actual duration of the sound")
    # format = { "source : { ...params... } , processors: [ { ...params... } ]"}
    parameters    = models.JSONField(default=None,null=True,blank=True,help_text="Parameters for this specific soundbite (source(if+processor parameters)")
    last_modified = models.DateTimeField(auto_now=True,null=True,help_text="the date/time the file was modified")
    record_date   = models.DateTimeField(auto_now_add=True,help_text="the date/time the file was entered in the database")

    # relation
    source        = models.ForeignKey(SoundTone,null=False,on_delete=models.CASCADE)
    processor     = models.ForeignKey(Processor,default=None,null=True,on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset,on_delete=models.CASCADE)

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

    @staticmethod
    def normalize_parameters(instance):
        pass
        # if instance.parameters is None:
        #     return
        # instance.parameters = json_normalize(instance.parameters)

    @staticmethod
    def pre_save(sender, instance, **kwargs):
        SoundBite.normalize_parameters(instance)

pre_save.connect(SoundBite.pre_save, SoundBite)              
    

