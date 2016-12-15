from django.http import HttpResponseRedirect, HttpResponse
from .models import User
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import *
from django.core.urlresolvers import reverse
import requests
import json

def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'login/detail.html', {'user': user})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(displayName=request.POST['displayName'], mail=request.POST['mail'], studentId=request.POST['studentId'])
            user.save()
            return HttpResponseRedirect(reverse('login:detail', args=(user.id,)))
    else:
        form = RegisterForm()
    return render(request, 'login/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            mail = request.POST['mail']
            password = request.POST['password']

            if(authenticate(mail, password)):
                user = User.objects.filter(mail=mail)
                if user.exists():
                    return HttpResponseRedirect(reverse('login:detail', args=(user.first().id,)))
                else:
                    return HttpResponseRedirect(reverse('login:register'))

    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})


def authenticate(mail, password):
    url = 'https://ucilnica.fri.uni-lj.si/login/index.php'
    data = {'username': mail, 'password': password}
    headers = {'Origin': 'ucilnica.fri.uni-lj.si',
               'Upgrade-Insecure-Requests': 1,
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Refer': 'https://ucilnica.fri.uni-lj.si/login/index.php',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'sl-SI,sl;q=0.8,en-GB;q=0.6,en;q=0.4,fi;q=0.2,hr;q=0.2',
               'Cookie': 'MoodleSession=7k4p5udvjh0slgfb02uohv0md2'
    }

    r = requests.post(url, data=json.dumps(data), headers=headers)

    #answer = json.loads(r.text)

    return True