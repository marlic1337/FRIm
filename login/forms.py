from django import forms

class RegisterForm(forms.Form):
    displayName = forms.CharField(max_length=20)
    mail = forms.CharField(max_length=30)
    studentId = forms.CharField(max_length=10)

class LoginForm(forms.Form):
    mail = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
