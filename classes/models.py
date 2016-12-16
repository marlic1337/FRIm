from django.db import models


class Predmet(models.Model):
    predmet_id = models.CharField(max_length=20, primary_key=True)
    predmet_name = models.CharField(max_length=100)
    predmet_category = models.CharField(max_length=10, default="razno")

    def __str__(self):
        return self.predmet_id + ' ' + self.predmet_name + ' ' + self.predmet_category

class Prostor(models.Model):
    prostor_id = models.CharField(max_length=20, primary_key=True)
    prostor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.prostor_name

class Profesor(models.Model):
    profesor_id = models.CharField(max_length=20, primary_key=True)
    profesor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.profesor_name

class Skupina(models.Model):
    skupina_id = models.CharField(max_length=20, primary_key=True)
    skupina_name = models.CharField(max_length=100)

    def __str__(self):
        return self.skupina_name

class Urnik(models.Model):
    urnik_name = models.CharField(max_length=100)

    def __str__(self):
        return self.urnik_name