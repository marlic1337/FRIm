from django.contrib import admin

from .models import Urnik, Profesor, Prostor, Predmet, Skupina

admin.site.register(Urnik)
admin.site.register(Profesor)
admin.site.register(Prostor)
admin.site.register(Predmet)
admin.site.register(Skupina)