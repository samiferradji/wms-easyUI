# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0011_auto_20161206_1420'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='achatsfournisseur',
            options={'permissions': (('valider_achats', 'Peut valider les achats'), ('voir_historique_achats', "Peut voir l'historique des achats"))},
        ),
        migrations.AlterModelOptions(
            name='transfert',
            options={'permissions': (('valider_mouvements_stock', 'Peut valider les mouvements de stocks'), ('transferer', 'Peut transferer'), ('entreposer', 'Peut Entreposer'), ('voir_historique_transferts', "Peut voir l'historique des transferts"), ('voir_stock', "Peut voir l'état du stock"), ('exporter_stock', "Peut exporter l'état du stock"))},
        ),
    ]
