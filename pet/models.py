from django.db import models
from django.utils import timezone
import datetime as dt
import humanize


class Pet(models.Model):
    name = models.CharField(max_length=200)
    date_of_birth = models.DateField()

    species_choices = [("dog", "Dog"), ("cat", "Cat")]
    gender_choices = [("m", "Male"), ("f", "Female")]

    species = models.CharField(max_length=200, choices=species_choices)
    breed = models.CharField(max_length=200)
    gender = models.CharField(max_length=200, choices=gender_choices)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def age(self):
        return humanize.precisedelta(dt.date.today() - self.date_of_birth)


class Event(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    pet = models.ForeignKey(Pet, on_delete=models.SET_NULL, null=True)

    event_choices = [
        ("nap", "Nap"),
        ("sleep", "Sleep"),
        ("eat", "Eat"),
        ("pee", "Pee"),
        ("poo", "Poo"),
        ("walk", "Walk"),
        ("wake", "Wake"),
        ("other", "Other"),
    ]
    event = models.CharField(max_length=200, choices=event_choices, default="pee")

    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(
            self.datetime().strftime("%Y-%m-%d %H:%M:%S"), self.event
        )

    def datetime(self):
        return dt.datetime.combine(self.date, self.time)