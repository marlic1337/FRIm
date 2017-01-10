from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import *

# Create your views here.

@login_required
def changeUserSettings(request):
    if not request.method == 'POST':
        form = ChangeUserSettings()
        title = 'Uporabniske nastavitve - ' + str(request.user.username)
        if request.user.email is 'emtpy@email.com':
            return render(request, 'User/user_settings.html', {'form': form, 'title': title, 'notificationsEmail': ''})
        else:
            return render(request, 'User/user_settings.html', {'form': form, 'title': title, 'notificationsEmail': str(request.user.email)})
