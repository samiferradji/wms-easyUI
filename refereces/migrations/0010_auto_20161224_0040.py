# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0009_auto_20161207_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeEntreposage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('type_entreposage', models.CharField(verbose_name="Types d'entreposage", max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='produit',
            name='seuil_max',
            field=models.IntegerField(verbose_name='Stock MAx', default=200),
        ),
        migrations.AddField(
            model_name='produit',
            name='seuil_min',
            field=models.IntegerField(verbose_name='Stock Min', default=50),
        ),
        migrations.AddField(
            model_name='produit',
            name='type_entreposage',
            field=models.ForeignKey(to='refereces.TypeEntreposage', null=True, blank=True),
        ),
    ]
