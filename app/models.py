from django.db import models
from datetime import timedelta

# Create your models here.

class Case(models.Model):
    case_num = models.PositiveIntegerField(unique=True)
    patient_name = models.CharField(max_length=200)
    id_num = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    date_of_onset = models.DateField()
    date_of_confirmation = models.DateField()

    def __str__(self):
        return self.patient_name

class Event(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    venue_name = models.CharField(max_length=200)
    venue_location = models.CharField(max_length=200)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    address = models.CharField(max_length=200)
    date = models.DateField()
    infector = models.BooleanField(default=False, editable=False)
    infected = models.BooleanField(default=False, editable=False)
    description = models.TextField()

    def __str__(self):
        return self.venue_name

    def save(self, *args, **kwargs):
        # Check for infector
        if self.date >= self.case.date_of_onset - timedelta(days=3) and self.date <= self.case.date_of_confirmation:
            self.infector = True
        # Check for infected
        if self.case.date_of_onset >= self.date + timedelta(days=2) and self.case.date_of_onset <= self.date + timedelta(days=14):
            self.infected = True
        super(Event, self).save(*args, **kwargs)