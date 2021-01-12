from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pet, Event
from .forms import EventForm

# from .analytics import import_csv
import humanize
import datetime as dt
import csv


def home(request, new_event=None):

    # if Event.objects.count() < 5:
    #     import_csv("~/projects/data-science/pet_diary_data.csv")

    pet = Pet.objects.first()

    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.pet = pet
            event.save()
            return redirect(home, new_event=event.pk)
        else:
            form = EventForm()
            return render(request, "pet/home.html", {"form": form})

    yesterday = dt.date.today() - dt.timedelta(days=7)

    events = Event.objects.filter(date__gte=yesterday).order_by("date", "time")[::-1][
        :20
    ]

    last_pee = Event.objects.filter(event="pee").order_by("-date", "-time")[0]
    time_from_last_pee = humanize.precisedelta(dt.datetime.now() - last_pee.datetime())

    last_poo = Event.objects.filter(event="poo").order_by("-date", "-time")[0]
    time_from_last_poo = humanize.precisedelta(dt.datetime.now() - last_poo.datetime())

    last_wake = Event.objects.filter(event="wake").order_by("-date", "-time")[0]
    time_from_last_wake = humanize.precisedelta(
        dt.datetime.now() - last_wake.datetime()
    )

    form = EventForm()

    return render(
        request,
        "pet/home.html",
        {
            "name": pet.name,
            "age": pet.age,
            "species": pet.species,
            "gender": pet.gender,
            "breed": pet.breed,
            "events": events,
            "event_choices": Event.event_choices,
            "form": form,
            "new_event": 0 if new_event is None else new_event,
            "time_from_last_pee": time_from_last_pee,
            "time_from_last_poo": time_from_last_poo,
            "time_from_last_wake": time_from_last_wake,
        },
    )


def delete_event(request, delete_event=None):
    event = Event.objects.filter(id=delete_event).delete()
    return redirect(home)


def download_csv(request):
    queryset = Event.objects.all()
    model = queryset.model
    model_fields = model._meta.fields + model._meta.many_to_many
    field_names = [field.name for field in model_fields]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="export.csv"'

    writer = csv.writer(response, delimiter=",")
    writer.writerow(field_names)

    for row in queryset:
        values = []
        for field in field_names:
            value = getattr(row, field)
            if callable(value):
                try:
                    value = value() or ""
                except:
                    value = "Error retrieving value"
            if value is None:
                value = ""
            values.append(value)
        writer.writerow(values)
    return response