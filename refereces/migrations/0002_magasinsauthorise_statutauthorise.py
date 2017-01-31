# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('refereces', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MagasinsAuthorise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('magasins', models.ForeignKey(verbose_name='Magasin Authorisé', to='refereces.Magasin')),
                ('user', models.ForeignKey(verbose_name='Utilisateur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StatutAuthorise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('magasins', models.ForeignKey(verbose_name='Magasin Authorisé', to='refereces.Magasin')),
                ('user', models.ForeignKey(verbose_name='Utilisateur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
