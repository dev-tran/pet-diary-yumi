from django import forms
from django.contrib.admin import widgets

from .models import Pet, Event


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TimeInput):
    input_type = "time"


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            "date",
            "time",
            "event",
            "detail",
        )
        widgets = {
            "date": DateInput({"class": "input is-horizontal field"}),
            "time": TimeInput({"class": "input is-horizontal field"}),
            "event": forms.Select({"class": "input is-horizontal field"}),
            "detail": forms.TextInput(
                attrs={"rows": 1, "cols": 50, "class": "input is-horizontal field"}
            ),
        }
