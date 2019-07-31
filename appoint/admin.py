"""
Admin classes for the  appoint application
"""
#######################################################################

from django.contrib import admin

from .forms import AppointmentForm
from .models import AppointeeType, Appointment, Notificant, Notification


#######################################################################
#######################################################################
#######################################################################


class NotificantInline(admin.TabularInline):
    model = Notificant
    extra = 1


#######################################################################


class AppointeeTypeAdmin(admin.ModelAdmin):
    """
    Admin interface for appointment types.
    """

    inlines = [NotificantInline]
    list_display = ["flag", "active"]
    list_filter = ["active", "modified", "created"]


admin.site.register(AppointeeType, AppointeeTypeAdmin)


#######################################################################


class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin interface for appointments (term positions).
    """

    form = AppointmentForm
    list_display = ["person", "start_date", "end_date", "active"]
    list_search = ["person__cn"]
    list_filter = ["active", "end_date", "start_date", "modified", "created"]


admin.site.register(Appointment, AppointmentAdmin)


#######################################################################
