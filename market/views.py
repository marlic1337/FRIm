from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from classes.views import parseUrnikVpisna, parseUrnikPredmet
from classes.models import Predmet, Prostor, Profesor
from User.models import CustomUser
from .models import PonudbaStudenta


def index(request):
    context = { }

    return render(request, 'market/index.html', context)

def makeoffer(request):
    urnik = parseUrnikVpisna(request.user.studentId)

    subjects = list()
    for u in urnik:
        predmet = Predmet.objects.get(predmet_id=u.subjectId)
        if predmet not in subjects and u.type == 'LV':
            subjects.append(predmet)

    context = {
        'subjects': subjects
    }
    return render(request, 'market/makeoffer.html', context)


def createoffer(request, subjectId):
    user = request.user
    subject = Predmet.objects.get(predmet_id=subjectId).predmet_name
    days = {
        'MON': 'ponedeljek',
        'TUE': 'torek',
        'WED': 'sreda',
        'THU': 'cetrtek',
        'FRI': 'petek',
    }

    urnik = parseUrnikVpisna(user.studentId)
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
        'id': user.studentId,
        'subject': subject,
        'offered_class': offered_class,
        'classroom': classroom,
        'teacher': teacher,
        'labs': labs_list,
        'labsListLength': len(labs_list)
    }

    return render(request, 'market/createoffer.html', context)

def myoffers(request):
    user = request.user
    offers = user.ponudbastudenta_set.all()

    context = {
        'offers': offers
    }

    return render(request, 'market/myoffers.html', context)


def migrateOffer(request):
    try:
        user = request.user
        offeredClass = request.POST['classInfo']
        subject = request.POST['subject']
        wish = request.POST['choice']
    except KeyError:
        subjectId = Predmet.objects.get(predmet_name=subject).predmet_id
        return render(request, 'market/nochoice.html', {'subjectId':subjectId})
    else:
        user.ponudbastudenta_set.create(studentSubject=subject, studentOffer=offeredClass, studentWish=wish, accepted=False, acceptedBy="0")

        context = {}
        return render(request, 'market/offercreated.html', context)


    #return HttpResponseRedirect(reverse('market:myoffers', args=()))

def alloffers(request):
    user = request.user
    offers = PonudbaStudenta.objects.exclude(user=user, accepted=True)
    #offers = PonudbaStudenta.objects.all()

    context = {
        'offers': offers
    }

    return render(request, 'market/alloffers.html', context)

def offeraccepted(request):
    offer = PonudbaStudenta.objects.get(pk=request.POST['offer'])
    offer.accepted = True
    offer.acceptedBy = request.user.studentId
    offer.save()

    context = {}

    return render(request, 'market/offeraccepted.html', context)

def nochoice(request):
    return render(request, 'market/nochoice.html', {})

def timetable(request):
    user = request.user
    urnik = parseUrnikVpisna(user.studentId)

    days = {
        'MON': 'ponedeljek',
        'TUE': 'torek',
        'WED': 'sreda',
        'THU': 'cetrtek',
        'FRI': 'petek',
    }

    type = {
        'P': 'predavanje',
        'LV': 'laboratorijske vaje',
    }

    for u in urnik:
        u.day = days[u.day]
        u.subjectId = Predmet.objects.get(predmet_id=u.subjectId).predmet_name
        u.classroom = Prostor.objects.get(prostor_id=u.classrooms[0]).prostor_name
        u.teacher = Profesor.objects.get(profesor_id=u.teachers[0]).profesor_name
        u.type = type[u.type]


    context = {
        'urnik': urnik
    }
    return render(request, 'market/timetable.html', context)
