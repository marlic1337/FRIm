from django.http import HttpResponse
from django.template import loader
from .models import Predmet
from .models import Profesor
from .models import Prostor
from .models import Skupina
from .models import Urnik
import requests
import re


def index(request):
    parseUrnik()
    #all_classes = Predmet.objects.all()
    #all_uni = Predmet.objects.all().filter(predmet_category="UNI")
    #all_vss = Predmet.objects.all().filter(predmet_category="VSS")
    #all_mag = Predmet.objects.all().filter(predmet_category="MAG")
    template = loader.get_template('classes/index.html')
    #context = {
    #    'all_classes': all_classes,
    #    'all_uni': all_uni,
    #    'all_vss': all_vss,
    #    'all_mag': all_mag,
    #}

    context = {
        'all_classes': Predmet.objects.all(),
        'all_teachers': Profesor.objects.all(),
        'all_classrooms': Prostor.objects.all(),
        'all_groups': Skupina.objects.all(),
        'urnik_name': Urnik.objects.all()[0],
    }

    return HttpResponse(template.render(context, request))

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