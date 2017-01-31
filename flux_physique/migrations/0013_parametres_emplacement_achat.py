# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0009_auto_20161207_1850'),
        ('flux_physique', '0012_auto_20161206_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametres',
            name='emplacement_achat',
            field=models.ForeignKey(to='refereces.Emplacement', null=True, verbose_name='Emplacement de reception des achats'),
        ),
    ]
