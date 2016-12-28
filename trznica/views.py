from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from classes.views import parseUrnikVpisna, parseUrnikPredmet
from classes.models import Predmet, Prostor, Profesor
from login.models import User
from .models import PonudbaStudenta


def index(request):
    context = {
        'options': ['Ponudbe', 'Moje ponudbe']
    }

    return render(request, 'trznica/index.html', context)

def makeoffer(request):
    urnik = parseUrnikVpisna('63140267')

    subjects = list()
    for u in urnik:
        predmet = Predmet.objects.get(predmet_id=u.subjectId)
        if predmet not in subjects and u.type == 'LV':
            subjects.append(predmet)

    context = {
        'subjects': subjects
    }
    return render(request, 'trznica/makeoffer.html', context)


def createoffer(request, subjectId):
    id = User.objects.get(pk=1).studentId
    subject = Predmet.objects.get(predmet_id=subjectId).predmet_name
    days = {
        'MON': 'ponedeljek',
        'TUE': 'torek',
        'WED': 'sreda',
        'THU': 'cetrtek',
        'FRI': 'petek',
    }

    urnik = parseUrnikVpisna(id)
    for u in urnik:
        if u.subjectId == subjectId and u.type == 'LV':
            offered_class = u
            offered_class.day = days[u.day[0:3]]
            classroom = Prostor.objects.get(prostor_id=u.classrooms[0]).prostor_name
            teacher = Profesor.objects.get(profesor_id=u.teachers[0]).profesor_name
            break


    labs = parseUrnikPredmet(offered_class.activitys[0])
    labs_list = list()
    for l in labs:
        l.day = days[l.day[0:3]]
        if not (l.day == offered_class.day and l.time == offered_class.time) and l.type == 'LV':
            l.classroom = Prostor.objects.get(prostor_id=l.classrooms[0]).prostor_name
            l.teacher = Profesor.objects.get(profesor_id=l.teachers[0]).profesor_name
            labs_list.append(l)

    context = {
        'id': id,
        'subject': subject,
        'offered_class': offered_class,
        'classroom': classroom,
        'teacher': teacher,
        'labs': labs_list,
    }

    return render(request, 'trznica/createoffer.html', context)

def myoffers(request):
    id = User.objects.get(pk=1).studentId
    offers = PonudbaStudenta.objects.all()

    context = {
        'offers': offers
    }

    return render(request, 'trznica/myoffers.html', context)


def migrateOffer(request):
    id = User.objects.get(pk=1).studentId
    try:
        offer = request.POST['choice']
        subject = request.POST['sub']
    except KeyError:
        return render(request, 'trznica/makeoffer.html', {'subjects': None})
    else:
        ponudba = PonudbaStudenta(studentId=id, studentSubject=subject, studentOffer=offer)
        ponudba.save()

        context = {}
        return render(request, 'trznica/offercreated.html', context)



    #return HttpResponseRedirect(reverse('trznica:myoffers', args=()))
