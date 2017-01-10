from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as logout_user

# Create your views here.
@login_required
def index(request):
    context = {
        'user': request.user,
        'title': 'FRIm Domaca Stran',
        'navbar_active': 'None'
    }
    return render(request, 'home/index.html', context)

def logout(request):
    logout_user(request)
    return HttpResponseRedirect('/')