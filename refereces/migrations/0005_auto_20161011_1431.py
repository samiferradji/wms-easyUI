# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('refereces', '0004_auto_20161010_0207'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepuisMagasinsAutorise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('magasins', models.ForeignKey(to='refereces.Magasin', verbose_name='Depuis : Magasins Autorisés')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='StatutsAutorise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('statuts', models.ForeignKey(to='refereces.StatutProduit', verbose_name='Statuts Autorisés')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='VersMagasinsAutorise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('magasins', models.ForeignKey(to='refereces.Magasin', verbose_name='Vers : Magasins Autorisés')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
        migrations.RemoveField(
            model_name='magasinsauthorise',
            name='magasins',
        ),
        migrations.RemoveField(
            model_name='magasinsauthorise',
            name='user',
        ),
        migrations.RemoveField(
            model_name='statutsauthorise',
            name='statuts',
        ),
        migrations.RemoveField(
            model_name='statutsauthorise',
            name='user',
        ),
        migrations.DeleteModel(
            name='MagasinsAuthorise',
        ),
        migrations.DeleteModel(
            name='StatutsAuthorise',
        ),
    ]
