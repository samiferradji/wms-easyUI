# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0016_transfert_motif'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='achatsfournisseur',
            options={'permissions': (('valider_achats', 'Peut valider les achats'), ('voir_historique_achats', "Peut voir l'historique des achats"), 'importer_achats', 'Peut importer les achats ')},
        ),
        migrations.AlterModelOptions(
            name='transfert',
            options={'permissions': (('valider_mouvements_stock', 'Peut valider les mouvements de stocks'), ('transferer', 'Peut transferer'), ('entreposer', 'Peut Entreposer'), ('voir_historique_transferts', "Peut voir l'historique des transferts"), ('voir_stock', "Peut voir l'état du stock"), ('exporter_stock', "Peut exporter l'état du stock"), ('sortie_colis_complets', "Peut fair des sorties en colis d'origine"))},
        ),
    ]
