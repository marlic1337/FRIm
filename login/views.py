from django.http import HttpResponseRedirect, HttpResponse
from .models import User
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import *
from django.core.urlresolvers import reverse
import requests
import re

def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'login/detail.html', {'user': user})

def registerOLD(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User(displayName=request.POST['displayName'], mail=request.POST['mail'], studentId=request.POST['studentId'])
            user.save()
            return HttpResponseRedirect(reverse('login:detail', args=(user.id,)))
    else:
        form = RegisterForm()
    return render(request, 'login/register.html', {'form': form})

def loginOLD(request):
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
                return render(request, 'login/loginFailed.html')

    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

def login(request):
    if not request.method == 'POST':
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'login/loginFailed.html') #ERROR! invalid form request!

    mail = request.POST['mail']
    user = authenticate(mail, request.POST['password'])
    if (user[0] == None or user[1] == None):
        return render(request, 'login/loginFailed.html') #ERROR! incomplete user data!
    elif (user[2] == None):
        return render(request, 'login/loginInvalidStudentId.html')  # ERROR! invalid student id!

    localUser = User.objects.filter(mail=mail)
    if localUser.count() == 0:
        register(mail, user)
    elif localUser.count() == 1:
        updateUserData(mail, user, localUser[0])
    else:
        return render(request, 'login/login.html') #ERROR! duplicated email

    localUser = User.objects.get(mail=mail)
    return detail(request, localUser.id)

def register(mail, user):
    localUser = User(displayName=user[1], mail=mail, studentId=user[2])
    localUser.save()

def updateUserData(mail, user, localUser):
    localUser.displayName = user[1]
    localUser.studentId = user[2]
    localUser.save()


def authenticate(mail, password):
    loginUrl = 'https://ucilnica.fri.uni-lj.si/login/index.php'

    response = requests.post(loginUrl, dict(username=mail, password=password, verify=False, allow_redirects=False))
    cookies = dict(MoodleSession=response.request._cookies['MoodleSession'])

    if (response.url != 'https://ucilnica.fri.uni-lj.si/my/'):
        return False

    #parse name and profile id
    profile = re.findall(r'Prijavljeni ste kot <a href="https://ucilnica.fri.uni-lj.si/user/profile.php\?id=(\d+)" title="Poglej profil">(.*?)</a>', response.content)

    id = int(profile[0][0])
    username = profile[0][1].title()

    #get student id
    editProfileUrl = 'https://ucilnica.fri.uni-lj.si/user/edit.php?id=' + str(id)
    response = requests.get(editProfileUrl, cookies=cookies, verify=False)

    studentId = re.findall(r'<input maxlength="255" size="25" name="idnumber" type="text" value="(\d{8})" id="id_idnumber" />', response.content)
    if not len(studentId) == 1:
        studentId = None
    else:
        studentId = studentId[0]

    return (id, username, studentId)