from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core import validators
from .forms import *
from models import CustomUser as MyUser
from models import SocialNetworks as sn

# Create your views here.

@login_required
def changeUserSettings(request):
    if not request.method == 'POST':
        form = ChangeUserSettings()
        title = 'Uporabniske nastavitve - ' + str(request.user.username)
        #if request.user.email is 'emtpy@email.com':
            #return render(request, 'User/user_settings.html', {'form': form, 'title': title, 'notificationsEmail': ''})
        #else:
        return render(request, 'User/user_settings.html', {'form': form, 'title': title, 'notificationsEmail': str(request.user.email)})

    form = ChangeUserSettings(request.POST, request.FILES)

    try:
        if not form.is_valid():
            return HttpResponseRedirect('/user/settings')
    except:
        return HttpResponseRedirect('/user/settings')

    currUser = MyUser.objects.get(username=request.user.username)
    mail = request.POST['email']

    if mail is u'' or u'@' in mail:
        currUser.email = mail

    soc_net = sn(user=request.user)
    url_facebook = request.POST['url_facebook']
    url_googleplus = request.POST['url_googleplus']
    url_twitter = request.POST['url_twitter']
    url_linkedin = request.POST['url_linkedin']
    url_github = request.POST['url_github']

    if 'facebook.com' in str(url_facebook) and ' ' not in str(url_facebook):
        soc_net.url_facebook = url_facebook

    if 'plus.google.com' in str(url_googleplus) and ' ' not in str(url_googleplus):
        soc_net.url_googleplus = url_googleplus

    if 'twitter.com' in str(url_twitter) and ' ' not in str(url_twitter):
        soc_net.url_twitter = url_twitter

    if 'linkedin.com' in str(url_linkedin) and ' ' not in str(url_linkedin):
        soc_net.url_linkedin = url_linkedin

    if 'github.com' in str(url_github) and ' ' not in str(url_github):
        soc_net.url_github = url_github

    soc_net.save()
    try:
        pic = request.FILES['logo']
        if pic is not None and 'image/' in pic.content_type:
            currUser.logo = pic
    except:
        pass

    currUser.save()

    return HttpResponseRedirect('/user/settings')
