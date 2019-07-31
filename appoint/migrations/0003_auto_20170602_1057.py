# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-02 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("appoint", "0002_auto_20150611_1516")]

    operations = [
        migrations.AlterModelOptions(
            name="appointeetype",
            options={"base_manager_name": "objects", "ordering": ("flag",)},
        ),
        migrations.AlterModelOptions(
            name="appointment",
            options={
                "base_manager_name": "objects",
                "ordering": ("person", "end_date"),
            },
        ),
        migrations.AlterModelOptions(
            name="notificant", options={"base_manager_name": "objects"}
        ),
        migrations.AlterModelOptions(
            name="notification", options={"base_manager_name": "objects"}
        ),
        migrations.AlterModelOptions(
            name="notificationmethod", options={"base_manager_name": "objects"}
        ),
        migrations.AlterField(
            model_name="notificant",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="appoint.AppointeeType"
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="appoint.AppointeeType"
            ),
        ),
    ]