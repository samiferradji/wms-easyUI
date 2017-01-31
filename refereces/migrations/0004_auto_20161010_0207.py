# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('refereces', '0003_auto_20161010_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statutsauthorise',
            name='statuts',
            field=models.ForeignKey(verbose_name='Statuts Authorisés', to='refereces.StatutProduit'),
        ),
    ]
