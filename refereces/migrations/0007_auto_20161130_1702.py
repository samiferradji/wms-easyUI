# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0006_auto_20161113_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dci',
            name='dci',
            field=models.CharField(max_length=50, verbose_name='DCI'),
        ),
    ]
