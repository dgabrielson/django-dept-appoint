# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("people", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="AppointeeType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="creation time"
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="last modification time"
                    ),
                ),
                (
                    "flag",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        to="people.PersonFlag",
                        help_text="The person flag corresponding to this type",
                        unique=True,
                    ),
                ),
            ],
            options={"ordering": ("flag",)},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="creation time"
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="last modification time"
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "message",
                    models.TextField(
                        help_text="An extra message for notificants regarding this appointment",
                        blank=True,
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        help_text="Only people in an appointee type are shown",
                        to="people.Person",
                    ),
                ),
            ],
            options={"ordering": ("person", "end_date")},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Notificant",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="creation time"
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="last modification time"
                    ),
                ),
                (
                    "near_threshold",
                    models.PositiveSmallIntegerField(
                        default=45,
                        help_text="The number of days in advance of the end of the appointment that the notification will be sent to the contact",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        help_text='Only people with the "appointee-notificant" flag are shown',
                        to="people.Person",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="appoint.AppointeeType"
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="creation time"
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="last modification time"
                    ),
                ),
                ("date", models.DateField()),
                (
                    "appointment",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="appoint.Appointment"
                    ),
                ),
                (
                    "notificant",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="people.Person"
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="appoint.AppointeeType"
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="NotificationMethod",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="creation time"
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True, verbose_name="last modification time"
                    ),
                ),
                ("method", models.CharField(max_length=16)),
                ("success", models.BooleanField(default=False)),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE, to="appoint.Notification"
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
    ]
