from django import forms
from .models import SoundSource , SoundTone , SoundBite
from .core.audio import get_audio_input_interfaces
from .core.midi import get_midi_output_ports , get_midi_input_ports
from .models import choice_midi_bank , choice_midi_program
import json

class SoundSourceForm(forms.ModelForm):
    # we need to handle the file path separately so that django doesnt automatically check that it exists...
    file_path = forms.CharField(max_length=512, required=False, help_text="The file path for the plugin or the recordings directory")
    #file_path = forms.FileField(max_length=512, required=False, help_text="The file path for the plugin or the recordings directory")
    audio_device_name = forms.CharField(widget=forms.Select(choices=get_audio_input_interfaces),required=False,max_length=64,help_text="Audio input device")
    midi_out_port_name = forms.CharField(widget=forms.Select(choices=get_midi_output_ports),required=False,max_length=64,help_text="MIDI OUT port name")
    # midi_in_port_name = forms.CharField(widget=forms.Select(choices=get_midi_input_ports),max_length=64,help_text="MIDI IN port name")

    field_order = [
        'type',
        'nature',
        'synthesis',
        'name',
        'description',
        'audio_device_name',
        'audio_device_samplerate',
        'audio_device_channels',
        'audio_device_kernelsize',
        'audio_device_sample_format',
        'midi_out_port_name',
#        'midi_in_port_name',
        'midi_channel',
        'parameters',
        'filenames',
        'file_path'
    ]        

    class Meta:
        model = SoundSource
        exclude = ['file_path','audio_device_name','midi_out_port_name','midi_in_port_name']  # Exclude the original file_path field from the model

    def __init__(self, *args, **kwargs):
        super(SoundSourceForm, self).__init__(*args, **kwargs)
        
        # Set initial value for file_path field if instance is provided and has a file_path attribute
        if self.instance and hasattr(self.instance, 'file_path'):
            self.fields['file_path'].initial = self.instance.file_path        
        if self.instance and hasattr(self.instance, 'audio_device_name'):
            self.fields['audio_device_name'].initial = self.instance.audio_device_name        
        if self.instance and hasattr(self.instance, 'midi_out_port_name'):
            self.fields['midi_out_port_name'].initial = self.instance.midi_out_port_name        

    def save(self, commit=True):
        instance = super(SoundSourceForm, self).save(commit=False)
        instance.file_path = self.cleaned_data.get('file_path')
        instance.audio_device_name = self.cleaned_data.get('audio_device_name')
        instance.midi_out_port_name = self.cleaned_data.get('midi_out_port_name')
        # instance.midi_in_port_name = self.cleaned_data.get('midi_in_port_name')
        if commit:
            instance.save()
        return instance
    


class SoundToneForm(forms.ModelForm):

    # we need to handle the file path separately so that django doesnt automatically check that it exists...
    #recording = forms.CharField(max_length=512, required=False, help_text="File path for recorded sources")
    # midi_bank     = forms.IntegerField(disabled=True,help_text="The MIDI bank of the sound")
    # midi_program  = forms.IntegerField(disabled=True,help_text="The MIDI program of the sound")
    tags = forms.CharField(max_length=128,widget=forms.Textarea,required=False,help_text="Tags associated with the sound")

    field_order = [
        # 'midi_bank',
        # 'midi_program',
        'name',
        'category',
        'description',
        'description_tech',
        'tags',
        'rec_duration',
        'rec_midi_range',
        'parameters'
    ]        

    class Meta:
        model = SoundTone
        exclude = ['recording','last_modified','record_date','midi_bank_msb','midi_bank_lsb','midi_program','source','tags'] 

    def __init__(self, *args, **kwargs):
        super(SoundToneForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.fields['category'].choices = self.instance.get_compatible_categories()
        try:
            if self.instance and hasattr(self.instance, 'tags'):
                tagsvalues = []
                for tag in self.instance.tags.all():
                    tagsvalues.append({"id":tag.id,"name":tag.tag})
                self.fields['tags'].initial = json.dumps(tagsvalues)
        except:
            self.fields['tags'].initial = "[]"

        # for visible in self.visible_fields():
        #     if visible.name in ['rec_duration','rec_midi_range']:
        #         visible.field.widget.attrs['class'] = 'half_size'            
        
        # Set initial value for file_path field if instance is provided and has a file_path attribute
        # if self.instance and hasattr(self.instance, 'midi_bank'):
        #     self.fields['midi_bank'].initial = self.instance.midi_bank        
        # if self.instance and hasattr(self.instance, 'midi_program'):
        #     self.fields['midi_program'].initial = self.instance.midi_program  

        # self.fields['midi_bank'].choices = choice_midi_bank()
        # self.fields['midi_program'].choices = choice_midi_program()      

    def save(self, commit=True):
        try:
            instance = super(SoundToneForm, self).save(commit=False)
            #instance.recording = self.cleaned_data.get('recording')
            if commit:
                instance.save()
            return instance
        except ValueError as e:
            print(e)