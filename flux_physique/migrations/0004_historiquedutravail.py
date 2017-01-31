# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0006_auto_20161113_1447'),
        ('flux_physique', '0003_auto_20161113_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoriqueDuTravail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('groupe', models.SmallIntegerField(verbose_name='Effectif du groupe')),
                ('employer', models.ForeignKey(to='refereces.Employer', verbose_name='Employer', on_delete=django.db.models.deletion.PROTECT)),
                ('id_validation', models.ForeignKey(to='flux_physique.Validation', verbose_name='ID Validation')),
                ('type', models.ForeignKey(to='refereces.TypesMouvementStock', verbose_name='Type du mouvement de stock', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
