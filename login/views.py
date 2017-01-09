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
        return render(request, 'login/loginFailed.html') #ERROR! invalid form request!

    mail = request.POST['mail']
    auth = User.CustomAuth.CustomAuth()
    user = auth.authenticate(username=mail, password=request.POST['password'])
    authLogin(request, user, 'User.CustomAuth.CustomAuth')

    if user is None:
        return render(request, 'login/loginFailed.html')

    if next:
        return HttpResponseRedirect(next)

    return HttpResponseRedirect('/')
