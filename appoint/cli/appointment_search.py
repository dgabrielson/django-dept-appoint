#######################
from __future__ import unicode_literals, print_function

#######################
#######################################################################

from optparse import make_option

HELP_TEXT = "Search for  AppointModel objects"
DJANGO_COMMAND = "main"
OPTION_LIST = (
    make_option(
        "--no-detail",
        action="store_false",
        dest="show-detail",
        default=True,
        help="By default, when only one result is returned, details will be printed also.  Giving this flag supresses this behaviour",
    ),
)
ARGS_USAGE = "[search terms]"

#######################################################################

from ..models import Appointment as Model
from . import object_detail


#######################################################################


def main(options, args):
    obj_list = Model.objects.search(*args)
    if options["show-detail"] and obj_list.count() == 1:
        obj = obj_list.get()
        object_detail(obj)
    else:
        for obj in obj_list:
            print("{}".format(obj.pk) + "\t" + "{}".format(obj))


#######################################################################
