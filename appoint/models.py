"""
Models for the appoint application.
"""
from __future__ import print_function, unicode_literals

import datetime
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from . import conf
from .managers import (
    AppointeeTypeManager,
    AppointmentManager,
    NotificantManager,
    NotificationManager,
    NotificationMethodManager,
)

#######################################################################
#######################################################################
#######################################################################


class AppointBaseModel(models.Model):
    """
    An abstract base class.
    """

    active = models.BooleanField(default=True)
    created = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_("creation time")
    )
    modified = models.DateTimeField(
        auto_now=True, editable=False, verbose_name=_("last modification time")
    )

    class Meta:
        abstract = True


#######################################################################
#######################################################################
#######################################################################


@python_2_unicode_compatible
class AppointeeType(AppointBaseModel):
    """
    An AppointeeType is a group of people which have appointments.
    """

    flag = models.OneToOneField(
        "people.PersonFlag",
        on_delete=models.CASCADE,
        help_text=_("The person flag corresponding to this type"),
    )

    objects = AppointeeTypeManager()

    class Meta:
        ordering = ("flag",)
        base_manager_name = "objects"

    def __str__(self):
        return "{}".format(self.flag)

    def get_absolute_url(self):
        """
        Get a url for this appointee type
        """
        return reverse("appoint-appointeetype-detail", kwargs={"pk": self.pk})


#######################################################################


@python_2_unicode_compatible
class Notificant(AppointBaseModel):
    """
    An appointee manager receives notifications about upcoming and current
    end_dates.
    """

    type = models.ForeignKey(AppointeeType, on_delete=models.PROTECT)
    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        limit_choices_to={"active": True, "flags__slug": "appointee-notificant"},
        help_text=_('Only people with the "appointee-notificant" flag are shown'),
    )
    near_threshold = models.PositiveSmallIntegerField(
        default=45,
        help_text=_(
            "The number of days in advance of the end of the appointment that the notification will be sent to the contact"
        ),
    )

    objects = NotificantManager()

    class Meta:
        base_manager_name = "objects"

    def __str__(self):
        return "{}".format(self.person.email)


#######################################################################


@python_2_unicode_compatible
class Appointment(AppointBaseModel):
    """
    A description of this model.
    """

    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        help_text=_("Only people in an appointee type are shown"),
    )
    start_date = models.DateField()
    end_date = models.DateField()
    message = models.TextField(
        blank=True,
        help_text=_("An extra message for notificants regarding this appointment"),
    )

    objects = AppointmentManager()

    class Meta:
        ordering = ("person", "end_date")
        base_manager_name = "objects"

    def __str__(self):
        return "{}".format(self.person)

    def get_absolute_url(self):
        """
        Get a url for this appointment
        """
        return reverse("appoint-appointment-detail", kwargs={"pk": self.pk})

    def get_types(self):
        """
        Get a queryset of appointee types for this appointment
        """
        return AppointeeType.objects.filter(flag__in=self.person.flags.active())

    def is_current(self, dt=None):
        """
        Return ``True`` if the appointment is current, relative to the given
        value of ``dt``.
        If ``dt`` is not specified, ``datetime.date.today()`` will be used.
        """
        if dt is None:
            dt = datetime.date.today()
        return self.start_date <= dt < self.end_date

    def is_expired(self, dt=None):
        """
        Return ``True`` if the appointment is expired, relative to the given
        value of ``dt``.
        If ``dt`` is not specified, ``datetime.date.today()`` will be used.
        """
        if dt is None:
            dt = datetime.date.today()
        return self.end_date <= dt


#######################################################################


@python_2_unicode_compatible
class Notification(AppointBaseModel):
    """
    A record of notification
    """

    notificant = models.ForeignKey("people.Person", on_delete=models.CASCADE)
    type = models.ForeignKey(AppointeeType, on_delete=models.PROTECT)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    date = models.DateField()

    objects = NotificationManager()

    class Meta:
        base_manager_name = "objects"

    def __str__(self):
        return "Notification to {0}".format(self.notificant)

    def send(self, method):
        """
        Attempt to send the notification by the given method.
        """
        method, created = NotificationMethod.objects.get_or_create(
            notification=self, method=method
        )
        if not method.success:
            method.send()

    def message(self, method, extra_context=None):
        """
        Return the text of the rendered message...
        """
        template_list = [
            "appoint/notification/{0}.txt".format(method),
            "appoint/notification/__base.txt",
        ]
        context = {
            "notificant": self.notificant,
            "type": self.type,
            "appointment": self.appointment,
            "date": self.date,
            "method": method,
            "expires_today": self.date == datetime.date.today(),
        }
        if extra_context:
            context.update(extra_context)

        return render_to_string(template_list, context)


#######################################################################


@python_2_unicode_compatible
class NotificationMethod(AppointBaseModel):
    """
    How someone gets notified.
    """

    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    method = models.CharField(max_length=16)
    success = models.BooleanField(default=False)

    objects = NotificationMethodManager()

    class Meta:
        base_manager_name = "objects"

    def __str__(self):
        return "{0} by {1}".format(self.notification, self.method)

    def send(self):
        """
        Send this notification by the appropriate method.
        Set and save success flag appropriately.
        """
        notification_methods = conf.get("notification_methods")
        if self.method not in notification_methods:
            raise ImproperlyConfigured(
                "The notification method {0!r} is not registered.".format(self.method)
            )
        module_name, method_name = notification_methods[self.method].rsplit(".", 1)
        module = import_module(module_name)
        method = getattr(module, method_name, None)
        if method is None:
            raise ImproperlyConfigured(
                "The notification method {0!r} was not found!".format(self.method)
            )
        text = self.notification.message(self.method)
        self.success = method(self.notification, text)
        self.save()


#######################################################################
