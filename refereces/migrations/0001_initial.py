# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Axe',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('axe', models.CharField(max_length=50, verbose_name='Axe de livraion', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('dossier', models.CharField(max_length=20, verbose_name='Dossier Client', unique=True)),
                ('nom_prenom', models.CharField(max_length=50, verbose_name='Nom Complet du client', unique=True)),
                ('adresse', models.CharField(max_length=100, verbose_name='Adresse de livraion')),
                ('telephone', models.CharField(max_length=30, verbose_name='Téléphone')),
                ('axe', models.ForeignKey(to='refereces.Axe', on_delete=django.db.models.deletion.PROTECT, verbose_name='Axe de livaion')),
            ],
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('code_commune', models.PositiveSmallIntegerField(null=True, verbose_name='Code', unique=True)),
                ('commune', models.CharField(max_length=50, verbose_name='Nom de la commune', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dci',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('code_dci', models.CharField(max_length=30, verbose_name='Code DCI', unique=True)),
                ('dci', models.CharField(max_length=30, verbose_name='DCI')),
                ('dosage', models.CharField(max_length=20, verbose_name='Dosage')),
            ],
        ),
        migrations.CreateModel(
            name='Emplacement',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('emplacement', models.CharField(max_length=10, verbose_name='Emplacement', unique=True)),
                ('volume', models.DecimalField(null=True, verbose_name='Capacité en volume', decimal_places=2, max_digits=10)),
                ('poids', models.DecimalField(null=True, verbose_name='Charge Maximale', decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('code_RH', models.CharField(max_length=10, verbose_name='Code RH', unique=True)),
                ('nom', models.CharField(max_length=50, verbose_name='Nom et prénom')),
            ],
        ),
        migrations.CreateModel(
            name='FormePharmaceutique',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('forme', models.CharField(max_length=30, verbose_name='Forme Pharmaceutique', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Founisseur',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('dossier', models.CharField(max_length=10, verbose_name='Dossier fournisseur', unique=True)),
                ('nom', models.CharField(max_length=50, verbose_name='Fournisseur', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoriqueDuTravail',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('groupe', models.SmallIntegerField(verbose_name='Effectif du groupe')),
                ('employer', models.ForeignKey(to='refereces.Employer', on_delete=django.db.models.deletion.PROTECT, verbose_name='Employer')),
            ],
        ),
        migrations.CreateModel(
            name='Laboratoire',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('dossier', models.CharField(null=True, max_length=10, verbose_name='Dossier laboratoire', unique=True)),
                ('nom', models.CharField(max_length=50, verbose_name='Laboratoire', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Magasin',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('magasin', models.CharField(max_length=30, verbose_name='Magasin', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('code', models.CharField(max_length=10, verbose_name='Code du produit', unique=True)),
                ('produit', models.CharField(max_length=50, verbose_name='Désignation du produit', unique=True)),
                ('conditionnement', models.CharField(max_length=10, verbose_name='Conditionnement')),
                ('poids', models.DecimalField(null=True, verbose_name='Poids', decimal_places=2, max_digits=10)),
                ('volume', models.DecimalField(null=True, verbose_name='Volume', decimal_places=2, max_digits=10)),
                ('thermosensible', models.BooleanField(verbose_name='Produit thermolabile')),
                ('psychotrope', models.BooleanField(verbose_name='Produit psychotrope')),
                ('a_rique', models.BooleanField(verbose_name='Produit à risque')),
                ('dci', models.ForeignKey(to='refereces.Dci', on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='DCI')),
                ('laboratoire', models.ForeignKey(to='refereces.Laboratoire', on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='Laboratoire')),
                ('prelevement', models.ForeignKey(to='refereces.Emplacement', on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='Emplacement de prélèvement')),
            ],
        ),
        migrations.CreateModel(
            name='StatutDocument',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('statut', models.CharField(max_length=30, verbose_name='Statut Document', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatutProduit',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('statut', models.CharField(max_length=30, verbose_name='Statut produit', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypesMouvementStock',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(max_length=50, verbose_name='Type du mouvement', unique=True)),
                ('niveau', models.SmallIntegerField(verbose_name='Niveau de difficulté')),
                ('description', models.TextField(null=True, verbose_name='Description du mouvement')),
            ],
        ),
        migrations.CreateModel(
            name='Wilaya',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('code_wilaya', models.PositiveSmallIntegerField(verbose_name='Code Wilaya', unique=True)),
                ('wilaya', models.CharField(max_length=50, verbose_name='Nom de Wilaya', unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='historiquedutravail',
            name='type',
            field=models.ForeignKey(to='refereces.TypesMouvementStock', on_delete=django.db.models.deletion.PROTECT, verbose_name='Type du mouvement de stock'),
        ),
        migrations.AddField(
            model_name='emplacement',
            name='magasin',
            field=models.ForeignKey(to='refereces.Magasin', on_delete=django.db.models.deletion.PROTECT, verbose_name='Magasin'),
        ),
        migrations.AddField(
            model_name='dci',
            name='forme_phrmaceutique',
            field=models.ForeignKey(to='refereces.FormePharmaceutique', on_delete=django.db.models.deletion.PROTECT, verbose_name='Forme pharmaceutique'),
        ),
        migrations.AddField(
            model_name='commune',
            name='wilaya',
            field=models.ForeignKey(to='refereces.Wilaya', on_delete=django.db.models.deletion.PROTECT, verbose_name='Wilaya'),
        ),
        migrations.AddField(
            model_name='client',
            name='commune',
            field=models.ForeignKey(to='refereces.Commune', on_delete=django.db.models.deletion.PROTECT, verbose_name='Commune'),
        ),
    ]
