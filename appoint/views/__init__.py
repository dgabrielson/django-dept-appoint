"""
Views for the appoint application
"""
#######################################################################

from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required, permission_required

from people.models import Person
from .formset import ProcessModelInlineFormsetMixin
from ..forms import AppointmentForm, AppointeeTypeForm, NotificantFormSet
from ..models import Appointment, AppointeeType


#######################################################################
#######################################################################


class AppointmentMixin(object):
    """
    Mixin for Appointment objects.
    """

    form_class = AppointmentForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.notificant_person = Person.objects.get_by_user(request.user)
        self.appointee_types = AppointeeType.objects.for_person(
            self.notificant_person
        ).active()
        if not self.appointee_types.exists():
            raise PermissionDenied
        return super(AppointmentMixin, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Restrict the queryset to appointments the requesting user
        will receive notifications for.
        """
        qs = Appointment.objects.active().for_notificant_person(self.notificant_person)
        return qs

    def get_form_kwargs(self):
        """
        Restrict the model form to the requesting user's AppointeeTypes.
        """
        kwargs = super(AppointmentMixin, self).get_form_kwargs()
        kwargs["notificiant_person"] = self.notificant_person
        return kwargs


#######################################################################


class AppointmentListView(AppointmentMixin, ListView):
    """
    List the appointments
    """


#######################################################################


class AppointmentDetailView(AppointmentMixin, DetailView):
    """
    Detail for the appointment
    """


#######################################################################


class AppointmentCreateView(AppointmentMixin, CreateView):
    """
    Create a new appointment
    """

    template_name = "appoint/appointment_create.html"


#######################################################################


class AppointmentUpdateView(AppointmentMixin, UpdateView):
    """
    Update an existing Appointment
    """

    template_name = "appoint/appointment_update.html"


#######################################################################


class AppointmentDeleteView(AppointmentMixin, DeleteView):
    """
    Delete an existing Appointment
    """

    def get_success_url(self):
        return reverse_lazy("appoint-appointment-list")


#######################################################################
#######################################################################


class AppointeeTypeMixin(object):
    """
    A mixin for all AppointeeType views.
    """

    form_class = AppointeeTypeForm
    queryset = AppointeeType.objects.active()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AppointeeTypeMixin, self).dispatch(*args, **kwargs)


#######################################################################


class AppointeeTypeListView(AppointeeTypeMixin, ListView):
    """
    List the AppointeeTypes
    """


#######################################################################


class AppointeeTypeDetailView(AppointeeTypeMixin, DetailView):
    """
    Detail for the AppointeeType
    """


#######################################################################


class AppointeeTypeCreateView(
    AppointeeTypeMixin, ProcessModelInlineFormsetMixin, CreateView
):
    """
    Create a new AppointeeType
    """

    template_name = "appoint/appointeetype_create.html"
    formset_class = NotificantFormSet

    @method_decorator(permission_required("appoint.add_appointeetype"))
    def dispatch(self, *args, **kwargs):
        return super(AppointeeTypeCreateView, self).dispatch(*args, **kwargs)


#######################################################################


class AppointeeTypeUpdateView(
    AppointeeTypeMixin, ProcessModelInlineFormsetMixin, UpdateView
):
    """
    Update an existing AppointeeType
    """

    template_name = "appoint/appointeetype_update.html"
    formset_class = NotificantFormSet

    @method_decorator(permission_required("appoint.change_appointeetype"))
    def dispatch(self, *args, **kwargs):
        return super(AppointeeTypeUpdateView, self).dispatch(*args, **kwargs)


#######################################################################


class AppointeeTypeDeleteView(AppointeeTypeMixin, DeleteView):
    """
    Delete an existing AppointeeType
    """

    @method_decorator(permission_required("appoint.delete_appointeetype"))
    def dispatch(self, *args, **kwargs):
        return super(AppointeeTypeDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("appoint-appointeetype-list")


#######################################################################
#######################################################################
#######################################################################
