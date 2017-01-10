from django import forms

class LoginForm(forms.Form):
    mail = forms.CharField(label='Email', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
