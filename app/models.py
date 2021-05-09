from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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