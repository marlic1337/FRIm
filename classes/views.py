from django.http import HttpResponse
from django.template import loader
from .models import Predmet


def index(request):
    all_classes = Predmet.objects.all()
    all_uni = Predmet.objects.all().filter(predmet_category="UNI")
    all_vss = Predmet.objects.all().filter(predmet_category="VSS")
    all_mag = Predmet.objects.all().filter(predmet_category="MAG")
    template = loader.get_template('classes/index.html')
    context = {
        'all_classes' : all_classes,
        'all_uni':all_uni,
        'all_vss': all_vss,
        'all_mag': all_mag,
    }
    return HttpResponse(template.render(context, request))