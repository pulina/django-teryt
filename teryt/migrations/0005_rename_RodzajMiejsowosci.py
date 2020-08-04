# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('teryt', '0004_set_aktywny_not_null'),
    ]

    operations = [
        migrations.RenameModel('RodzajMiejsowosci', 'RodzajMiejscowosci'),
    ]
