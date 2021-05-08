from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import json
from urllib.parse import urljoin

# Create your models here.

class CHPuser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_number = models.CharField(max_length=6)

    class Meta:
        verbose_name = "CHP User"
        verbose_name_plural = "CHP Users"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            CHPuser.objects.create(user=instance)
        instance.chpuser.save()

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
        url = "https://geodata.gov.hk/gs/api/v1.0.0/locationSearch"

        temp = str(self.venue_location)
        query = "?q=" + temp.replace(" ","%20")
        final_url = urljoin(url, query)
        r = requests.get(url = final_url)
        if r.status_code == 200:
            data = r.json() 
            data = data[0]
            self.address = data['addressEN']
            self.x_coordinate =  float(data['x'])
            self.y_coordinate =  float(data['y'])
        else:
            self.x_coordinate =  0.0
            self.y_coordinate =  0.0
            self.address = "-"  

        # Check for infector
        if self.date >= self.case.date_of_onset - timedelta(days=3) and self.date <= self.case.date_of_confirmation:
            self.infector = True
        # Check for infected
        if self.case.date_of_onset >= self.date + timedelta(days=2) and self.case.date_of_onset <= self.date + timedelta(days=14):
            self.infected = True
        super(Event, self).save(*args, **kwargs)