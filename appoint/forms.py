"""
Forms for the appoint application.
"""
#######################################################################

from django import forms
from django.db import models
from django.forms.models import inlineformset_factory

from django.contrib.admin import widgets

from . import conf
from .models import Appointment, AppointeeType, Notificant, Notification


#######################################################################


class AppointmentForm(forms.ModelForm):
    """
    This restricts the person selection to people who are in any of the 
    appointee groups..  
    """

    def __init__(self, *args, **kwargs):
        """
        Restrict selection of people to those available (plus the
        currently select person, if any).
        """
        notificant_person = kwargs.pop("notificiant_person", None)
        super(AppointmentForm, self).__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)  # an Appointment
        PersonField = self.fields["person"]
        person = None
        if instance is not None:
            person = instance.person
        PersonField.queryset = AppointeeType.objects.available_people(instance=person)
        # self.notificant_person = notificiant_person
        if notificant_person is not None:
            PersonField.queryset = AppointeeType.objects.for_person(
                notificant_person
            ).available_people(instance=person)

    class Meta:
        model = Appointment
        exclude = ["active"]
        widgets = {
            "start_date": widgets.AdminDateWidget,
            "end_date": widgets.AdminDateWidget,
        }

    class Media:
        css = {"all": ("admin/css/widgets.css", "css/forms.css")}
        js = [
            conf.get("jsi18n_url"),
            "admin/js/core.js",
            "admin/js/vendor/jquery/jquery.js",
            "admin/js/jquery.init.js",
            "admin/js/calendar.js",
            "admin/js/admin/DateTimeShortcuts.js",
        ]


#######################################################################


class AppointeeTypeForm(forms.ModelForm):
    """
    Form for appointee groups.
    """

    class Meta:
        model = AppointeeType
        fields = ["active", "flag"]

    class Media:
        css = {"all": ("admin/css/widgets.css", "css/forms.css")}


#######################################################################


class NotificantForm(forms.ModelForm):
    """
    Form for appointee groups.
    """

    class Meta:
        model = Notificant
        exclude = []


#######################################################################

NotificantFormSet = inlineformset_factory(
    AppointeeType, Notificant, form=NotificantForm, extra=1
)

#######################################################################


class NotificationForm(forms.ModelForm):
    """
    Form for appointee groups.
    """

    class Meta:
        model = Notification
        exclude = []


#######################################################################
