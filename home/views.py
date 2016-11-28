from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def index(request):
    all_users = User.objects.all()
    template = loader.get_template('home/index.html')
    context = {
        'all_users': all_users,
        'invalid_user': all_users.count() + 1,
    }

    return HttpResponse(template.render(context, request))

def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    template = loader.get_template('home/detail.html')
    context = {
        'user': user,
    }

    return HttpResponse(template.render(context, request))
