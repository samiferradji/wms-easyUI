# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('refereces', '0002_magasinsauthorise_statutauthorise'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatutsAuthorise',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('statuts', models.ForeignKey(verbose_name='Statuts Authorisés', to='refereces.Magasin')),
                ('user', models.ForeignKey(verbose_name='Utilisateur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='statutauthorise',
            name='magasins',
        ),
        migrations.RemoveField(
            model_name='statutauthorise',
            name='user',
        ),
        migrations.AlterField(
            model_name='magasinsauthorise',
            name='magasins',
            field=models.ForeignKey(verbose_name='Magasins Authorisés', to='refereces.Magasin'),
        ),
        migrations.DeleteModel(
            name='StatutAuthorise',
        ),
    ]
