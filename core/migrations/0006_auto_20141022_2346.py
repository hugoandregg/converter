# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141021_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='titulo',
            field=models.CharField(max_length=30),
        ),
    ]
