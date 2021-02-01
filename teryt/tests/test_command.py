#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from django.core import management
from django.test import TestCase

from teryt.models import RodzajMiejscowosci, JednostkaAdministracyjna, Miejscowosc, Ulica


class TestParseCommand(TestCase):

    files = [
        "teryt/tests/assets/SIMC_Adresowy_2020-07-29.zip",
        "teryt/tests/assets/TERC_Adresowy_2020-07-29.zip",
        "teryt/tests/assets/ULIC_Adresowy_2020-07-29.zip",
        "teryt/tests/assets/WMRODZ_2020-07-29.zip",
    ]

    def test_command(self):
        management.call_command('teryt_parse', *self.files)
        self.assertTrue(RodzajMiejscowosci.objects.count())
        self.assertTrue(JednostkaAdministracyjna.objects.count())
        self.assertTrue(Miejscowosc.objects.count())
        self.assertTrue(Ulica.objects.count())

    def tearDown(self):
        # Unittest has problems with destroying Miejscowosc
        Ulica.objects.all().delete()
        Miejscowosc.objects.filter(miejscowosc_nadrzedna__isnull=False).delete()
        Miejscowosc.objects.all().delete()
        JednostkaAdministracyjna.objects.all().delete()
        RodzajMiejscowosci.objects.all().delete()
