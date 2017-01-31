# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0008_auto_20161204_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achatsfournisseur',
            name='validate_by',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='validation_achats'),
        ),
        migrations.AlterField(
            model_name='transfert',
            name='validate_by',
            field=models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, related_name='validation_name'),
        ),
    ]
