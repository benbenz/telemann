from django import forms
from .models import SoundSource , SoundTone , SoundBite
from .core.audio import get_audio_input_interfaces
from .core.midi import get_midi_output_ports , get_midi_input_ports

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

    field_order = [
        'category',
        'description',
        'tags',
        'parameters'
    ]        

    class Meta:
        model = SoundTone
        exclude = ['recording','last_modified','record_date','midi_bank','midi_program','parameters','generator'] 

    def __init__(self, *args, **kwargs):
        super(SoundToneForm, self).__init__(*args, **kwargs)
        
        # Set initial value for file_path field if instance is provided and has a file_path attribute
        # if self.instance and hasattr(self.instance, 'recording'):
        #     self.fields['recording'].initial = self.instance.recording        

    def save(self, commit=True):
        instance = super(SoundToneForm, self).save(commit=False)
        #instance.recording = self.cleaned_data.get('recording')
        if commit:
            instance.save()
        return instance