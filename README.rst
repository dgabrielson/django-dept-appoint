django-dept-appoint
=====================

A django application for tracking term appointments that 
are either expiring or require periodic notifications.

Enabling the standard ``appoint.urls`` and views for this application
allow people who are going to be notified ("notificants")
to managed their own appointments.

Additionally, if you enable ``appoint.urls.appointeetypes`` then
people who have the standard 
``appoint.{add,change,delete}_appointeetype`` permissions can 
perform those actions without the django admin (or the staff flag).
The ``appoint.change_appointeetype`` is checked in the default templates
to access the list of appointee types.  (I.e., change is treated as 
equivalent to view access.)

Note that the corresponding view classes all assume you are using
``django.contrib.auth`` in a relatively standard way.