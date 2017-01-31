# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flux_physique', '0002_transfert_statut_doc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('id_in_content_type', models.PositiveIntegerField(verbose_name='Id in content type')),
                ('content_type', models.PositiveIntegerField(verbose_name='Contenent type')),
                ('boite_count', models.PositiveIntegerField(verbose_name='Nombre de boites')),
                ('ligne_count', models.PositiveIntegerField(verbose_name='Nombre de lignes')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='transfert',
            name='validate_by',
            field=models.ForeignKey(related_name='validation_name', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
