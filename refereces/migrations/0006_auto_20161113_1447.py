# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0005_auto_20161011_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historiquedutravail',
            name='employer',
        ),
        migrations.RemoveField(
            model_name='historiquedutravail',
            name='type',
        ),
        migrations.DeleteModel(
            name='HistoriqueDuTravail',
        ),
    ]
