#######################
from __future__ import unicode_literals, print_function

#######################
#######################################################################

HELP_TEXT = "Get detail on an AppointModel object, including related objects"
DJANGO_COMMAND = "main"
OPTION_LIST = ()
ARGS_USAGE = "pk [pk [...]]"

#######################################################################

from ..models import Appointment as Model
from . import object_detail

M2M_FIELDS = []
RELATED_ONLY = None  # Specify a list or None; None means introspect for related
RELATED_EXCLUDE = []  # any related fields to skip


#######################################################################


def main(options, args):
    for pk in args:
        # get the object
        obj = Model.objects.get(pk=pk)
        print(object_detail(obj, M2M_FIELDS, RELATED_ONLY, RELATED_EXCLUDE))


#######################################################################
