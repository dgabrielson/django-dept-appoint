"""
The url patterns for the appoint application.

These urls allow for anyone with the standard add,change,delete
permissions on AppointeeTypes to manage them.
"""
#######################################################################

from django.conf.urls import url

from ..views import (
    AppointeeTypeListView,
    AppointeeTypeDetailView,
    AppointeeTypeCreateView,
    AppointeeTypeUpdateView,
    AppointeeTypeDeleteView,
)


#######################################################################

urlpatterns = [
    url(r"^$", AppointeeTypeListView.as_view(), name="appoint-appointeetype-list"),
    url(
        r"^(?P<pk>\d+)/$",
        AppointeeTypeDetailView.as_view(),
        name="appoint-appointeetype-detail",
    ),
    url(
        r"^new/$",
        AppointeeTypeCreateView.as_view(),
        name="appoint-appointeetype-create",
    ),
    url(
        r"^(?P<pk>\d+)/update/$",
        AppointeeTypeUpdateView.as_view(),
        name="appoint-appointeetype-update",
    ),
    url(
        r"^(?P<pk>\d+)/delete/$",
        AppointeeTypeDeleteView.as_view(),
        name="appoint-appointeetype-delete",
    ),
]


#######################################################################
