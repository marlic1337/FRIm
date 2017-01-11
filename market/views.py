# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import smart_text
from django.core.mail import send_mail
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from classes.views import parseUrnikVpisna, parseUrnikPredmet
from classes.models import Predmet, Prostor, Profesor
from User.models import CustomUser
from .models import PonudbaStudenta

@login_required
def index(request):
    context = {'active_nav': 'market'}

    return render(request, 'market/index.html', context)

@login_required
def makeoffer(request):
    urnik = parseUrnikVpisna(request.user.studentId)

    subjects = list()
    for u in urnik:
        predmet = Predmet.objects.get(predmet_id=u.subjectId)
        if predmet not in subjects and u.type == 'LV':
            subjects.append(predmet)

    context = {
        'active_nav': 'market',
        'subjects': subjects
    }
    return render(request, 'market/makeoffer.html', context)

@login_required
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
            try:
                teacher = Profesor.objects.get(profesor_id=u.teachers[0]).profesor_name
            except:
                teacher = Profesor.objects.get(profesor_id="Neznan").profesor_name
            break


    labs = parseUrnikPredmet(offered_class.activitys[0])
    labs_list = list()
    for l in labs:
        l.day = days[l.day[0:3]]
        if not (l.day == offered_class.day and l.time == offered_class.time) and l.type == 'LV':
            l.classroom = Prostor.objects.get(prostor_id=l.classrooms[0]).prostor_name
            try:
                l.teacher = Profesor.objects.get(profesor_id=l.teachers[0]).profesor_name
            except:
                teacher = Profesor.objects.get(profesor_id="Neznan").profesor_name
            labs_list.append(l)

    context = {
        'active_nav': 'market',
        'id': user.studentId,
        'subject': subject,
        'offered_class': offered_class,
        'classroom': classroom,
        'teacher': teacher,
        'labs': labs_list,
        'labsListLength': len(labs_list)
    }

    return render(request, 'market/createoffer.html', context)

@login_required
def myoffers(request):
    user = request.user
    acceptedTrue = user.ponudbastudenta_set.filter(accepted=True)
    acceptedFalse = user.ponudbastudenta_set.filter(accepted=False)


    context = {
        'active_nav': 'market',
        'acceptedTrue': acceptedTrue,
        'acceptedFalse': acceptedFalse,
    }

    return render(request, 'market/myoffers.html', context)

@login_required
def migrateOffer(request):
    try:
        user = request.user
        offeredClass = request.POST['classInfo']
        subject = request.POST['subject']
        wish = request.POST['choice']
    except KeyError:
        subjectId = Predmet.objects.get(predmet_name=subject).predmet_id
        return render(request, 'market/nochoice.html', {'active_nav': 'market','subjectId':subjectId})
    else:
        context = {'active_nav': 'market',}

        if request.user.ponudbastudenta_set.filter(studentSubject=subject).count() == 0:
            user.ponudbastudenta_set.create(studentSubject=subject, studentOffer=offeredClass, studentWish=wish, accepted=False, acceptedBy="0")
            return render(request, 'market/offercreated.html', context)
        else:
            return render(request, 'market/oneoffer.html', context)


    #return HttpResponseRedirect(reverse('market:myoffers', args=()))

@login_required
def alloffers(request):
    user = request.user
    offers = PonudbaStudenta.objects.exclude(user=user).exclude(accepted=True)
    #offers = PonudbaStudenta.objects.all()
    query_text = None
    if request.method == 'GET' and 'query' in request.GET.keys():
        query_text = request.GET['query']
        for string in query_text.split(" "):
            offers = offers.filter(studentSubject__icontains=string)
    context = {
        'active_nav': 'market',
        'offers': offers,
        'query_text': query_text,
    }

    return render(request, 'market/alloffers.html', context)

@login_required
def offeraccepted(request):
    offer = PonudbaStudenta.objects.get(pk=request.POST['offer'])
    offer.accepted = True
    offer.acceptedBy = request.user.studentId
    offer.save()

    if offer.user.email != '':
        email = offer.user.email
    else:
        email = offer.user

    send_mail('Ponudba za predmet {} je bila sprejeta'.format(offer.studentSubject),
              format_html('Pozdravljeni!\n\nVaša ponudba na FRIm za predmet {} je bila sprejeta.\n\nPrejšnji termin vaj: {}\nNovi termin vaj: {}'
                '\n\nPosodobljen urnik si lahko ogledate na https://frimarket.herokuapp.com/urnik/.\n\n'
                'Lep Pozdrav, FRIm'.format(offer.studentSubject, offer.studentOffer, offer.studentWish)),
              'frim.mailer@gmail.com',
              ['{}'.format(email)], fail_silently=False)

    context = {
        'active_nav': 'market',
    }

    return render(request, 'market/offeraccepted.html', context)

@login_required
def nochoice(request):
    return render(request, 'market/nochoice.html', {'active_nav': 'market'})

@login_required
def oneoffer(request):
    return render(request, 'market/oneoffer.html', {'active_nav': 'market'})

@login_required
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

        unicode_text = smart_text('{}, {}; {}; {}'.format(u.day, u.time, u.classroom, u.teacher), encoding='utf-8', strings_only=False, errors='strict')
        #offerString = "{}, {}; {}; {}".format(u.time, u.day, u.classroom, u.teacher)


        try:
            if PonudbaStudenta.objects.filter(user=request.user, studentOffer=unicode_text, accepted=True).count() == 1:
                myAcceptedOffer = PonudbaStudenta.objects.get(user=request.user, studentOffer=unicode_text, accepted=True)

                if myAcceptedOffer.accepted:
                    u.day = myAcceptedOffer.studentWish.split('; ')[0].split(', ')[0]
                    u.time = myAcceptedOffer.studentWish.split('; ')[0].split(', ')[1]
                    u.classroom = myAcceptedOffer.studentWish.split('; ')[1]
                    u.teacher = myAcceptedOffer.studentWish.split('; ')[2]
            elif PonudbaStudenta.objects.filter(studentWish=unicode_text, accepted=True, acceptedBy=request.user.studentId).count() == 1:
                myAcceptedOffer = PonudbaStudenta.objects.get(studentWish=unicode_text, accepted=True, acceptedBy=request.user.studentId)

                if myAcceptedOffer.accepted:
                    u.day = myAcceptedOffer.studentOffer.split('; ')[0].split(', ')[0]
                    u.time = myAcceptedOffer.studentOffer.split('; ')[0].split(', ')[1]
                    u.classroom = myAcceptedOffer.studentOffer.split('; ')[1]
                    u.teacher = myAcceptedOffer.studentOffer.split('; ')[2]
        except PonudbaStudenta.DoesNotExist:
            pass

    context = {
        'active_nav': 'market',
        'urnik': urnik
    }
    return render(request, 'market/timetable.html', context)

@login_required
def deleteOffer(request):
    PonudbaStudenta.objects.get(pk=request.POST['offer']).delete()

    offers = request.user.ponudbastudenta_set.all()
    context = {
        'active_nav': 'market',
        'offers': offers
    }

    return render(request, 'market/deleteoffer.html', context)