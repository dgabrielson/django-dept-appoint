#######################
from __future__ import unicode_literals, print_function

#######################
#######################################################################

HELP_TEXT = "Send out any appropriate appointment notifications."
DJANGO_COMMAND = "main"
OPTION_LIST = ()
ARGS_USAGE = ""

#######################################################################

import datetime

from django.db import models

from ..models import Appointment, Notificant, Notification


#######################################################################


def main(options, args):
    verbosity = int(options["verbosity"])
    method_list = ["email"]
    today = datetime.date.today()
    threshold = list(
        Notificant.objects.active().aggregate(models.Max("near_threshold")).values()
    ).pop()
    dt = today + datetime.timedelta(days=threshold)
    for appointment in Appointment.objects.active().expired(dt):
        for appointee_type in appointment.get_types():
            for notificant in appointee_type.notificant_set.active():
                on_dt = today + datetime.timedelta(days=notificant.near_threshold)
                if appointment.is_expired(on_dt):
                    notice, created = Notification.objects.get_or_create(
                        notificant=notificant.person,
                        type=appointee_type,
                        appointment=appointment,
                        defaults={"date": today},
                    )
                    if created:
                        for method in method_list:
                            if verbosity > 1:
                                print(
                                    "Sending notification",
                                    appointment,
                                    appointee_type,
                                    notificant,
                                    method,
                                )
                            notice.send(method)


#######################################################################
