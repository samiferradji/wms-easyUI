# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0009_auto_20161204_1602'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='achatsfournisseur',
            options={'permissions': (('valider_mouvements_stock', 'Peut valider les mouvements de stocks'), ('transferer', 'Peut transferer'), ('entreposer', 'Peut Entreposer'), ('voir_historique', "Peut voir l'historique des transferts"), ('voir_stock', "Peut voir et exporter l'état du stock"))},
        ),
    ]
