# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0010_auto_20161224_0040'),
        ('flux_physique', '0015_auto_20161208_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfert',
            name='motif',
            field=models.ForeignKey(verbose_name='Motif du mouvement', to='refereces.TypesMouvementStock', default=1),
        ),
    ]
