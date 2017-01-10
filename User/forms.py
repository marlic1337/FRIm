from django import forms

class ChangeUserSettings(forms.Form):
    email = forms.CharField(label='Email za obvescanje', max_length=50, required=False)
    logo = forms.ImageField(required=False)

    # social networks urls
    url_facebook = forms.CharField(max_length=64, required=False)
    url_googleplus = forms.CharField(max_length=64, required=False)
    url_twitter = forms.CharField(max_length=64, required=False)
    url_linkedin = forms.CharField(max_length=64, required=False)
    url_github = forms.CharField(max_length=64, required=False)
