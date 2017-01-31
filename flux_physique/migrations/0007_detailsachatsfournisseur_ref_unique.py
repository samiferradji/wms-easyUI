# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0006_auto_20161130_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailsachatsfournisseur',
            name='ref_unique',
            field=models.CharField(verbose_name='reference_unique', max_length=20, default=0),
        ),
    ]
