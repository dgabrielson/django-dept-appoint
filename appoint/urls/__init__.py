"""
The url patterns for the appoint application.
These urls allow for notificants to manage their own appointments.
"""
#######################################################################

from django.conf.urls import url

from ..views import (
    AppointmentListView,
    AppointmentDetailView,
    AppointmentCreateView,
    AppointmentUpdateView,
    AppointmentDeleteView,
)


#######################################################################

urlpatterns = [
    url(r"^$", AppointmentListView.as_view(), name="appoint-appointment-list"),
    url(
        r"^(?P<pk>\d+)/$",
        AppointmentDetailView.as_view(),
        name="appoint-appointment-detail",
    ),
    url(r"^new/$", AppointmentCreateView.as_view(), name="appoint-appointment-create"),
    url(
        r"^(?P<pk>\d+)/update/$",
        AppointmentUpdateView.as_view(),
        name="appoint-appointment-update",
    ),
    url(
        r"^(?P<pk>\d+)/delete/$",
        AppointmentDeleteView.as_view(),
        name="appoint-appointment-delete",
    ),
]


#######################################################################
