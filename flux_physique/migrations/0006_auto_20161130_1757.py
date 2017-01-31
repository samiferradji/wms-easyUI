# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0005_reservation_new_emplacement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailsachatsfournisseur',
            name='poids_boite',
            field=models.DecimalField(verbose_name='Poids boite', default=0, decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='detailsachatsfournisseur',
            name='poids_colis',
            field=models.DecimalField(verbose_name='Poids du Colis', default=0, decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='detailsachatsfournisseur',
            name='volume_boite',
            field=models.DecimalField(verbose_name='Volume boite', default=0, decimal_places=2, max_digits=9),
        ),
    ]
