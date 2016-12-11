from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=60)
    description = forms.CharField(max_length=1000)
    file = forms.FileField(label='Izberi datoteko')

class UpdateFileForm(forms.Form):
    title = forms.CharField(max_length=60)
    description = forms.CharField(max_length=1000)