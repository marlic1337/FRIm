
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
import User.CustomAuth

from django.contrib.auth import login as authLogin

# Create your views here.
def login(request):
    next = request.POST.get('next', request.GET.get('next', ''))
    if not request.method == 'POST':
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form, 'next': next})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'login/loginFailedOld.html') #ERROR! invalid form request!

    mail = request.POST['mail']
    auth = User.CustomAuth.CustomAuth()

    try:
        request.POST['update_user']
        update = True
    except:
        update = False

    user = auth.authenticate(username=mail, password=request.POST['password'], update_user=update)

    if user is None:
        return render(request, 'login/loginFailedOld.html')

    if user.username == 'ucilnicaDown' or user.username == 'noStudentId' or user.username == 'incorrectCredentials':
        return render(request, 'login/login_failed.html', {'error': str(user.username)})

    authLogin(request, user, 'User.CustomAuth.CustomAuth')




    if next:
        return HttpResponseRedirect(next)

    return HttpResponseRedirect('/')
