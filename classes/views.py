from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.template import loader
from .models import Predmet
from .models import Profesor
from .models import Prostor
from .models import Skupina
from .models import Urnik
from market.models import PonudbaStudenta
import requests
import re
import operator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout as logout_user

@login_required
def index(request):
    parseUrnik()

    urnik = parseUrnikVpisna(request.user.studentId)

    # probably not working
    #for i in range (len(urnik)):
    #    try:
    #        if PonudbaStudenta.objects.get(pk=request.user.studentId).studentSubject == urnik[i].subjectId:
    #            if PonudbaStudenta.objects.get(pk=request.user.studentId).accepted:
    #                urnik[i] = PonudbaStudenta.objects.get(user=request.user.studentId).studentWish
    #    except ObjectDoesNotExist:
    #        continue


    template = loader.get_template('classes/index.html')

    all_classes = []
    all_cls = Predmet.objects.all()
    for cls in all_cls:
        all_classes.append(cls)
    all_classes_sorted = sorted(all_classes, key=operator.attrgetter('predmet_name'))

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
        #u.teacher = Profesor.objects.get(profesor_id=u.teachers[0]).profesor_name
        u.type = type[u.type]


    context = {
        'urnik': urnik,
        'all_classes': all_classes_sorted,
        'all_teachers': Profesor.objects.all(),
        'all_classrooms': Prostor.objects.all(),
        'all_groups': Skupina.objects.all(),
        'urnik_name': Urnik.objects.all()[0],
        'user': request.user,
        'title': 'FRIm Moj Urnik',
    }
    #return render(request, 'classes/index.html', context)
    return HttpResponse(template.render(context, request))


def logout(request):
    logout_user(request)
    return HttpResponseRedirect('/')


def parseUrnik():
    urnikUrl = 'https://urnik.fri.uni-lj.si/'

    response = requests.get(urnikUrl)

    currentUrnikName = re.findall(r'https://urnik\.fri\.uni-lj\.si/timetable/(.*?)/', response.url)
    if len(currentUrnikName) < 1:
        return False #PARSE ERROR

    currentUrnikName = currentUrnikName[0]
    u = Urnik.objects.filter(urnik_name=currentUrnikName)
    if len(u) > 0:
        return True #Urnik se ni spremenil

    Urnik.objects.all().delete()
    u = Urnik(urnik_name=currentUrnikName)
    u.save()

    teachers = re.findall(r'<a href= ".*?allocations\?teacher=(.*?)">(.*?)</a><br/>', response.content)
    print len(teachers)
    if len(teachers) < 1:
        return False #PARSE ERROR

    Profesor.objects.all().delete()
    for teacher in teachers:
        t = Profesor(teacher[0], teacher[1])
        t.save()

    classrooms = re.findall(r'<a href=".*?allocations\?classroom=(.*?)">(.*?)</a><br/>', response.content)
    print len(classrooms)
    if len(classrooms) < 1:
        return False #PARSE ERROR

    Prostor.objects.all().delete()
    for classroom in classrooms:
        c = Prostor(classroom[0], classroom[1])
        c.save()

    groups = re.findall(r'<a href=".*?allocations\?group=(.*?)">(.*?)</a><br/>', response.content)
    print len(groups)
    if len(groups) < 1:
        return False #PARSE ERROR

    Skupina.objects.all().delete()
    for group in groups:
        g = Skupina(group[0], group[1])
        g.save()

    subjects = re.findall(r'<a href=".*?allocations\?subject=(.*?)">(.*?)\(.*?\)</a><br/>', response.content)
    print len(subjects)
    if len(subjects) < 1:
        return False #PARSE ERROR

    Predmet.objects.all().delete()
    for subject in subjects:
        s = Predmet(subject[0], subject[1])
        s.save()

    return True


#
# Parse results:
# Step A:
#   [0]: time
#   [1]: data passed to step B
# Step B:
#   [0]: day (MON, TUE, WEN, THU, FRI)
#   [1]: type (P or LV)
#   [2]: duration in hours
#   [3]: subject ID
#   [4]: data passed to step C
# Step C:
#   [0]: data type(classroom, teacher, group, activity)
#   [1]: data id
#

def parseUrnikVpisna(studentId):
    uaList = list()
    urnikName = Urnik.objects.all()[0].urnik_name
    urnikUrl = 'https://urnik.fri.uni-lj.si/timetable/' + urnikName + '/allocations?student=' + studentId
    response = requests.get(urnikUrl)
    content = response.content.replace('\n', '').replace('\r', '').replace(' ', '')

    stepA = re.findall(r'<trclass="timetable"><tdclass="hour">(.*?)</td>(.*?)</tr>', content)
    for a in stepA:
        stepB = re.findall(r'<tdclass="(.*?)allocated(.*?)"colspan=.*?rowspan=(\d)><div><span>.*?\(.*?\).*?\((.*?)\).*?</span>(.*?)</div></td>', a[1])
        for b in stepB:
            ua = UrnikActivity()
            ua.time = a[0]
            ua.day = b[0][len(b[0])-3:len(b[0])]
            ua.duration = b[2]
            ua.type = b[1]
            ua.subjectId = b[3]
            ua.activitys = list()
            ua.classrooms = list()
            ua.teachers = list()
            ua.groups = list()

            if ua.day == 'MON':
                ua.ind = 1
            elif ua.day == 'TUE':
                ua.ind = 2
            elif ua.day == 'WED':
                ua.ind = 3
            elif ua.day == 'THU':
                ua.ind = 4
            elif ua.day == 'FRI':
                ua.ind = 5

            stepC = re.findall(r'<aclass=".*?"href="\?(.*?)=(.*?)">.*?</a><br/>', b[4])
            for c in stepC:
                if c[0] == 'activity':
                    ua.activitys.append(c[1])
                elif c[0] == 'classroom':
                    ua.classrooms.append(c[1])
                elif c[0] == 'teacher':
                    ua.teachers.append(c[1])
                elif c[0] == 'group':
                    ua.groups.append(c[1])

            uaList.append(ua)

    return uaList


def parseUrnikPredmet(activityId):
    uaList = list()
    urnikName = Urnik.objects.all()[0].urnik_name
    urnikUrl = 'https://urnik.fri.uni-lj.si/timetable/' + urnikName + '/allocations?activity=' + activityId
    response = requests.get(urnikUrl)
    content = response.content.replace('\n', '').replace('\r', '').replace(' ', '')

    stepA = re.findall(r'<trclass="timetable"><tdclass="hour">(.*?)</td>(.*?)</tr>', content)
    for a in stepA:
        stepB = re.findall(r'<tdclass="(.*?)allocated(.*?)"colspan=1rowspan=(\d{1})><div><span>.*?\(.*?\).*?\((.*?)\).*?</span>(.*?)</div></td>', a[1])
        for b in stepB:
            ua = UrnikActivity()
            ua.time = a[0]
            ua.day = b[0]
            ua.duration = b[2]
            ua.type = b[1]
            ua.subjectId = b[3]
            ua.activitys = list()
            ua.classrooms = list()
            ua.teachers = list()
            ua.groups = list()

            stepC = re.findall(r'<aclass=".*?"href="\?(.*?)=(.*?)">.*?</a><br/>', b[4])
            for c in stepC:
                if c[0] == 'activity':
                    ua.activitys.append(c[1])
                elif c[0] == 'classroom':
                    ua.classrooms.append(c[1])
                elif c[0] == 'teacher':
                    ua.teachers.append(c[1])
                elif c[0] == 'group':
                    ua.groups.append(c[1])

            uaList.append(ua)

    return uaList


class UrnikActivity:
    day = ''
    time = ''
    duration = 0
    type = ''
    subjectId = ''
    activitys = list()
    classrooms = list()
    teachers = list()
    groups = list()
    ind = 0
