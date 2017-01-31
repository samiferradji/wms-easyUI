# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flux_physique', '0014_auto_20161207_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='new_emplacement',
            field=models.ForeignKey(null=True, to='refereces.Emplacement'),
        ),
    ]
