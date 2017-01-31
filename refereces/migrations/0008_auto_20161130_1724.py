# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0007_auto_20161130_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='a_rique',
            field=models.BooleanField(default=False, verbose_name='Produit à risque'),
        ),
        migrations.AlterField(
            model_name='produit',
            name='conditionnement',
            field=models.CharField(default='B/', verbose_name='Conditionnement', max_length=10),
        ),
        migrations.AlterField(
            model_name='produit',
            name='prelevement',
            field=models.ForeignKey(default=1, to='refereces.Emplacement', null=True, verbose_name='Emplacement de prélèvement', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='produit',
            name='psychotrope',
            field=models.BooleanField(default=False, verbose_name='Produit psychotrope'),
        ),
        migrations.AlterField(
            model_name='produit',
            name='thermosensible',
            field=models.BooleanField(default=False, verbose_name='Produit thermolabile'),
        ),
    ]
