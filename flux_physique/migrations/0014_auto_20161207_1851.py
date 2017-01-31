# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0013_parametres_emplacement_achat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametres',
            name='emplacement_achat',
            field=models.ForeignKey(verbose_name='Emplacement de reception des achats', to='refereces.Emplacement', default=24),
            preserve_default=False,
        ),
    ]
