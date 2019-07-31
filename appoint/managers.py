"""
Managers for the appoint application.
"""
#######################################################################

from django.db import models


from .querysets import (
    AppointmentQuerySet,
    AppointeeTypeQuerySet,
    NotificantQuerySet,
    NotificationQuerySet,
    NotificationMethodQuerySet,
)


#######################################################################
#######################################################################
#######################################################################


class CustomQuerySetManager(models.Manager):
    """
    Custom Manager for an arbitrary model, just a wrapper for returning
    a custom QuerySet
    """

    queryset_class = models.query.QuerySet

    def get_queryset(self):
        """
        Return the custom QuerySet
        """
        return self.queryset_class(self.model)


#######################################################################
#######################################################################
#######################################################################


class AppointeeTypeManager(CustomQuerySetManager):
    queryset_class = AppointeeTypeQuerySet


AppointeeTypeManager = AppointeeTypeManager.from_queryset(
    AppointeeTypeManager.queryset_class
)

#######################################################################


class NotificantManager(CustomQuerySetManager):
    queryset_class = NotificantQuerySet


NotificantManager = NotificantManager.from_queryset(NotificantManager.queryset_class)

#######################################################################


class AppointmentManager(CustomQuerySetManager):
    queryset_class = AppointmentQuerySet


AppointmentManager = AppointmentManager.from_queryset(AppointmentManager.queryset_class)

#######################################################################


class NotificationManager(CustomQuerySetManager):
    queryset_class = NotificationQuerySet


NotificationManager = NotificationManager.from_queryset(
    NotificationManager.queryset_class
)

#######################################################################


class NotificationMethodManager(CustomQuerySetManager):
    queryset_class = NotificationMethodQuerySet


NotificationMethodManager = NotificationMethodManager.from_queryset(
    NotificationMethodManager.queryset_class
)

#######################################################################
