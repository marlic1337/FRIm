from django import forms

class ChangeUserSettings(forms.Form):
    email = forms.CharField(label='Email za obvescanje', max_length=50)

    # social networks urls
    url_facebook = forms.CharField(max_length=64)
    url_googleplus = forms.CharField(max_length=64)
    url_twitter = forms.CharField(max_length=64)
    url_linkedin = forms.CharField(max_length=64)
    url_github = forms.CharField(max_length=64)

class PostForm(forms.Form):
    subject = forms.CharField(max_length=60)
    body = forms.CharField(max_length=10000)


class PostEditForm(forms.Form):
    subject = forms.CharField(max_length=60)
    body = forms.CharField(max_length=10000)
    delete = forms.BooleanField(required=False)
