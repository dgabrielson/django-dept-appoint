"""
CLI list for appoint
"""
#######################
from __future__ import unicode_literals, print_function

#######################
#######################################################################
#######################################################################
from optparse import make_option

HELP_TEXT = __doc__.strip()
DJANGO_COMMAND = "main"
OPTION_LIST = (
    make_option(
        "-f",
        "--fields",
        dest="field_list",
        help="Specify a comma delimited list of fields to include, e.g., -f PROVIDE,EXAMPLE",
    ),
)
# ARGS_USAGE = '...'


#######################################################################

from . import resolve_fields
from ..models import Appointment as Model

#######################################################################


def main(options, args):

    qs = Model.objects.active()
    for item in qs:
        value_list = ["{}".format(item.pk), "{}".format(item)]
        if options["field_list"]:
            value_list += resolve_fields(item, options["field_list"].split(","))
        print("\t".join(value_list))


#######################################################################
