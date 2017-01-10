from django import forms

class ChangeUserSettings(forms.Form):
    email = forms.CharField(label='Email za obvescanje', max_length=50)
    img = forms.ImageField()

    # social networks urls
    url_facebook = forms.CharField(max_length=64)
    url_googleplus = forms.CharField(max_length=64)
    url_twitter = forms.CharField(max_length=64)
    url_linkedin = forms.CharField(max_length=64)
    url_github = forms.CharField(max_length=64)
