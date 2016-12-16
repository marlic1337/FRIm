from django.db import models


class Predmet(models.Model):
    predmet_id = models.CharField(max_length=20, primary_key=True)
    predmet_name = models.CharField(max_length=100)
    predmet_category = models.CharField(max_length=10, default="razno")

    def __str__(self):
        return self.predmet_id + ' ' + self.predmet_name + ' ' + self.predmet_category
