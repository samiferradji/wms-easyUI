# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0008_auto_20161130_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='conditionnement',
            field=models.CharField(max_length=10, null=True, verbose_name='Conditionnement', blank=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='poids',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name='Poids', blank=True),
        ),
        migrations.AlterField(
            model_name='produit',
            name='volume',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, verbose_name='Volume', blank=True),
        ),
    ]
