# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('refereces', '0008_auto_20161130_1724'),
        ('flux_physique', '0007_detailsachatsfournisseur_ref_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exercice', models.IntegerField(verbose_name='Exercice en cours')),
                ('magasin_picking', models.ForeignKey(verbose_name='Magasin de picking', to='refereces.Magasin')),
            ],
        ),
        migrations.AddField(
            model_name='achatsfournisseur',
            name='validate_by',
            field=models.ForeignKey(related_name='validation_achats', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
