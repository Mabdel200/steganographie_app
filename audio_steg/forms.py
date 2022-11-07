from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import PostFile


class FilesForm(ModelForm):
    class Meta:
        model = PostFile
        fields = ['type_file_id', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class DecryptForm(ModelForm):
    class Meta:
        model = PostFile
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


# upload file sender
class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')


# Steganographie  begin
class TextForm(forms.Form):
    stegtype = forms.CharField(max_length=10, widget=forms.HiddenInput(), initial='Text')
    CHOICES = (('1', 'Encrypt',), ('2', 'Decrypt'))
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='Choose Mode:', required=False,
                                     initial='1')
    plaintext = forms.CharField(label='Plain Text')
    hiddentext = forms.CharField(label='Hidden Text', max_length=35, required=False)

    class Meta:
        model = PostFile


class ImageForm(forms.Form):
    stegtype = forms.CharField(max_length=10, widget=forms.HiddenInput(), initial='Text')
    stegimage = forms.ImageField(label="Image")
    hiddentext = forms.CharField(label='Hidden Text', max_length=35)

    class Meta:
        model = PostFile


class AudioForm(forms.Form):
    stegtype = forms.CharField(max_length=10, widget=forms.HiddenInput(), initial='Text')
    CHOICES = (('1', 'Encrypt',), ('2', 'Decrypt'))
    choice_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label='Choose Mode:', required=False,
                                     initial='1')
    hiddentext = forms.CharField(label='Text')

    class Meta:
        model = PostFile
