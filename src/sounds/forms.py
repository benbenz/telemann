from django import forms
from .models import SoundGenerator

class SoundGeneratorForm(forms.ModelForm):
    # we need to handle the file path separately so that django doesnt automatically check that it exists...
    file_path = forms.CharField(max_length=512, required=False, help_text="File path for the plugin")

    class Meta:
        model = SoundGenerator
        exclude = ['file_path']  # Exclude the original file_path field from the model

    def save(self, commit=True):
        instance = super(SoundGeneratorForm, self).save(commit=False)
        instance.file_path = self.cleaned_data.get('file_path')
        if commit:
            instance.save()
        return instance