"""
Querysets for the appoint application.
"""
#######################
from __future__ import unicode_literals, print_function

#######################
#######################################################################

import datetime
from functools import reduce
import operator

from django.core.exceptions import ImproperlyConfigured
from django.db import models

from . import conf


#######################################################################
#######################################################################
#######################################################################


class BaseCustomQuerySet(models.query.QuerySet):
    """
    Custom QuerySet.
    """

    def active(self):
        """
        Returns only the active items in this queryset
        """
        return self.filter(active=True)

    def search(self, *criteria):
        """
        Magic search for objects.
        This is heavily modelled after the way the Django Admin handles
        search queries.
        See: django.contrib.admin.views.main.py:ChangeList.get_query_set
        """
        if not hasattr(self, "search_fields"):
            raise ImproperlyConfigured(
                "No search fields.  Provide a "
                "search_fields attribute on the QuerySet."
            )

        if len(criteria) == 0:
            assert False, "Supply search criteria"

        terms = ["{}".format(c) for c in criteria]
        if len(terms) == 1:
            terms = terms[0].split()

        def construct_search(field_name):
            if field_name.startswith("^"):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith("="):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith("@"):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        qs = self.filter(active=True)
        orm_lookups = [
            construct_search("{}".format(search_field))
            for search_field in self.search_fields
        ]
        for bit in terms:
            or_queries = [models.Q(**{orm_lookup: bit}) for orm_lookup in orm_lookups]
            qs = qs.filter(reduce(operator.or_, or_queries))

        return qs.distinct()


#######################################################################
#######################################################################
#######################################################################


class AppointeeTypeQuerySet(BaseCustomQuerySet):
    """
    Provide a custom model API.  Urls, views, etc. should only
    use these methods, never .filter(...).
    """

    search_fields = ["flag__slug", "flag__verbose_name"]

    def person_queryset(self):
        """
        Return a person query set corresponding to the current queryset
        of appointee groups.
        """
        from people.models import Person

        flag_set = self.values_list("flag", flat=True).distinct()
        return Person.objects.filter(flags__in=flag_set).distinct()

    def available_people(self, dt=None, instance=None):
        """
        Return a queryset of people that are available for appointments.

        If ``instance`` is not None, then presumably we are working
        with an existing form where there should be only the current
        person on the resulting queryset.
        
        If the setting ``exclude_current`` is True, then no currently
        appointed people will be considered.

        If dt is None, then ``datetime.date.today()`` is used to 
        determine "current".
        """
        qs = self.active().person_queryset().active()
        if instance:
            return qs.filter(pk=instance.pk)

        if conf.get("exclude_current"):
            if dt is None:
                dt = datetime.date.today()
            qs = qs.exclude(
                appointment__start_date__lte=dt, appointment__end_date__gt=dt
            )
        return qs

    def for_person(self, person):
        """
        Restricts queryset to the types the given person will be
        notified for.
        """
        return self.filter(notificant__person=person)


#######################################################################


class NotificantQuerySet(BaseCustomQuerySet):
    """
    Provide a custom model API.  Urls, views, etc. should only
    use these methods, never .filter(...).
    """

    search_fields = ["person__cn"]


#######################################################################


class AppointmentQuerySet(BaseCustomQuerySet):
    """
    Provide a custom model API.  Urls, views, etc. should only
    use these methods, never .filter(...).
    """

    search_fields = ["person__cn"]

    def current(self, dt=None):
        """
        Return the restricted queryset where ``start_date <= dt < end_date``.
        If ``dt`` is not given, then ``datetime.date.today()`` is used.
        """
        if dt is None:
            dt = datetime.date.today()
        return self.filter(start_date__lte=dt, end_date__gt=dt)

    def expired(self, dt=None):
        """
        Return the restricted queryset where end_date <= dt.
        If ``dt`` is not given, then ``datetime.date.today()`` is used.
        """
        if dt is None:
            dt = datetime.date.today()
        return self.filter(end_date__lte=dt)

    def for_notificant_person(self, person):
        """
        Restricts the queryset to appointments for whom the given person
        will receive notifications.
        """
        return self.filter(person__flags__appointeetype__notificant__person=person)


#######################################################################


class NotificationQuerySet(BaseCustomQuerySet):
    """
    Provide a custom model API.  Urls, views, etc. should only
    use these methods, never .filter(...).
    """

    search_fields = ["person__cn", "appointment__person__cn"]


#######################################################################


class NotificationMethodQuerySet(BaseCustomQuerySet):
    """
    Provide a custom model API.  Urls, views, etc. should only
    use these methods, never .filter(...).
    """

    # search_fields = ['person__cn', 'appointment__person__cn', ]


#######################################################################
