# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("appoint", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="appointeetype",
            name="flag",
            field=models.OneToOneField(
                on_delete=models.deletion.CASCADE,
                to="people.PersonFlag",
                help_text="The person flag corresponding to this type",
            ),
        )
    ]
