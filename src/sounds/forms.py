from django import forms
from .models import SoundGenerator
from .core.audio import get_audio_input_interfaces
from .core.midi import get_midi_output_ports , get_midi_input_ports

class SoundGeneratorForm(forms.ModelForm):
    # we need to handle the file path separately so that django doesnt automatically check that it exists...
    file_path = forms.CharField(max_length=512, required=False, help_text="The file path for the plugin or the recordings directory")
    #file_path = forms.FileField(max_length=512, required=False, help_text="The file path for the plugin or the recordings directory")
    audio_device_name = forms.CharField(widget=forms.Select(choices=get_audio_input_interfaces),max_length=64,help_text="Audio input device")
    midi_out_port_name = forms.CharField(widget=forms.Select(choices=get_midi_output_ports),required=False,max_length=64,help_text="MIDI OUT port name")
    # midi_in_port_name = forms.CharField(widget=forms.Select(choices=get_midi_input_ports),max_length=64,help_text="MIDI IN port name")

    field_order = [
        'type',
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
        model = SoundGenerator
        exclude = ['file_path','audio_device_name','midi_out_port_name','midi_in_port_name']  # Exclude the original file_path field from the model

    def save(self, commit=True):
        instance = super(SoundGeneratorForm, self).save(commit=False)
        instance.file_path = self.cleaned_data.get('file_path')
        instance.audio_device_name = self.cleaned_data.get('audio_device_name')
        instance.midi_out_port_name = self.cleaned_data.get('midi_out_port_name')
        # instance.midi_in_port_name = self.cleaned_data.get('midi_in_port_name')
        if commit:
            instance.save()
        return instance