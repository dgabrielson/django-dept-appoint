# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'NotificationMethod'
        db.create_table(
            u"appoint_notificationmethod",
            (
                (u"id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                (
                    "active",
                    self.gf("django.db.models.fields.BooleanField")(default=True),
                ),
                (
                    "created",
                    self.gf("django.db.models.fields.DateTimeField")(
                        auto_now_add=True, blank=True
                    ),
                ),
                (
                    "modified",
                    self.gf("django.db.models.fields.DateTimeField")(
                        auto_now=True, blank=True
                    ),
                ),
                (
                    "notification",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        to=orm["appoint.Notification"]
                    ),
                ),
                ("method", self.gf("django.db.models.fields.CharField")(max_length=16)),
                (
                    "success",
                    self.gf("django.db.models.fields.BooleanField")(default=False),
                ),
            ),
        )
        db.send_create_signal(u"appoint", ["NotificationMethod"])

        # Adding field 'Notification.type'
        db.add_column(
            u"appoint_notification",
            "type",
            self.gf("django.db.models.fields.related.ForeignKey")(
                default=1, to=orm["appoint.AppointeeType"]
            ),
            keep_default=False,
        )

    def backwards(self, orm):
        # Deleting model 'NotificationMethod'
        db.delete_table(u"appoint_notificationmethod")

        # Deleting field 'Notification.type'
        db.delete_column(u"appoint_notification", "type_id")

    models = {
        u"appoint.appointeetype": {
            "Meta": {"ordering": "('flag',)", "object_name": "AppointeeType"},
            "active": ("django.db.models.fields.BooleanField", [], {"default": "True"}),
            "created": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now_add": "True", "blank": "True"},
            ),
            "flag": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": u"orm['people.PersonFlag']", "unique": "True"},
            ),
            u"id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "modified": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now": "True", "blank": "True"},
            ),
        },
        u"appoint.appointment": {
            "Meta": {
                "ordering": "('person', 'end_date')",
                "object_name": "Appointment",
            },
            "active": ("django.db.models.fields.BooleanField", [], {"default": "True"}),
            "created": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now_add": "True", "blank": "True"},
            ),
            "end_date": ("django.db.models.fields.DateField", [], {}),
            u"id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "message": ("django.db.models.fields.TextField", [], {"blank": "True"}),
            "modified": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now": "True", "blank": "True"},
            ),
            "person": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": u"orm['people.Person']"},
            ),
            "start_date": ("django.db.models.fields.DateField", [], {}),
        },
        u"appoint.notificant": {
            "Meta": {"object_name": "Notificant"},
            "active": ("django.db.models.fields.BooleanField", [], {"default": "True"}),
            "created": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now_add": "True", "blank": "True"},
            ),
            u"id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "modified": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now": "True", "blank": "True"},
            ),
            "near_threshold": (
                "django.db.models.fields.PositiveSmallIntegerField",
                [],
                {"default": "45"},
            ),
            "person": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": u"orm['people.Person']"},
            ),
            "type": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": u"orm['appoint.AppointeeType']"},
            ),
        },
        u"appoint.notification": {
            "Meta": {"object_name": "Notification"},
            "active": ("django.db.models.fields.BooleanField", [], {"default": "True"}),
            "appointment": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": u"orm['appoint.Appointment']"},
            ),
            "created": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now_add": "True", "blank": "True"},
            ),
            "date": ("django.db.models.fields.DateField", [], {}),
            u"id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "modified": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now": "True", "blank": "True"},
            ),
            "notificant": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": u"orm['people.Person']"},
            ),
            "type": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": u"orm['appoint.AppointeeType']"},
            ),
        },
        u"appoint.notificationmethod": {
            "Meta": {"object_name": "NotificationMethod"},
            "active": ("django.db.models.fields.BooleanField", [], {"default": "True"}),
            "created": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now_add": "True", "blank": "True"},
            ),
            u"id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "method": ("django.db.models.fields.CharField", [], {"max_length": "16"}),
            "modified": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now": "True", "blank": "True"},
            ),
            "notification": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": u"orm['appoint.Notification']"},
            ),
            "success": (
                "django.db.models.fields.BooleanField",
                [],
                {"default": "False"},
            ),
        },
        u"people.person": {
            "Meta": {"ordering": "['sn', 'given_name']", "object_name": "Person"},
            "active": ("django.db.models.fields.BooleanField", [], {"default": "True"}),
            "birthday": (
                "django.db.models.fields.DateField",
                [],
                {"null": "True", "blank": "True"},
            ),
            "cn": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "100", "blank": "True"},
            ),
            "company": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "64", "blank": "True"},
            ),
            "created": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now_add": "True", "blank": "True"},
            ),
            "flags": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {
                    "symmetrical": "False",
                    "to": u"orm['people.PersonFlag']",
                    "null": "True",
                    "blank": "True",
                },
            ),
            "given_name": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "64"},
            ),
            u"id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "modified": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now": "True", "blank": "True"},
            ),
            "note": ("django.db.models.fields.TextField", [], {"blank": "True"}),
            "slug": (
                "django.db.models.fields.SlugField",
                [],
                {"max_length": "50", "unique": "True", "null": "True", "blank": "True"},
            ),
            "sn": ("django.db.models.fields.CharField", [], {"max_length": "64"}),
            "title": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "64", "blank": "True"},
            ),
            "username": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "30", "unique": "True", "null": "True", "blank": "True"},
            ),
        },
        u"people.personflag": {
            "Meta": {"ordering": "['verbose_name']", "object_name": "PersonFlag"},
            "active": ("django.db.models.fields.BooleanField", [], {"default": "True"}),
            "created": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now_add": "True", "blank": "True"},
            ),
            u"id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "modified": (
                "django.db.models.fields.DateTimeField",
                [],
                {"auto_now": "True", "blank": "True"},
            ),
            "slug": (
                "django.db.models.fields.SlugField",
                [],
                {"unique": "True", "max_length": "64"},
            ),
            "verbose_name": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "64"},
            ),
        },
    }

    complete_apps = ["appoint"]
