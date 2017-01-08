from django import forms

class LoginForm(forms.Form):
    mail = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
