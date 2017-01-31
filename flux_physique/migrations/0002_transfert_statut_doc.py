# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0005_auto_20161011_1431'),
        ('flux_physique', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfert',
            name='statut_doc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='refereces.StatutDocument', default=1, verbose_name='Statut du document'),
            preserve_default=False,
        ),
    ]
