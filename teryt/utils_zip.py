from collections import OrderedDict
import io
import os.path
import zipfile
import re
import requests
from django.core.management.base import CommandError
from django.db import transaction, DatabaseError, IntegrityError

from .models import (RodzajMiejscowosci, JednostkaAdministracyjna,
                    Miejscowosc, Ulica)
from .utils import get_xml_id_dictionary, parse

# Dictionary containing teryt data files and according 
# data models inside them. Order is crucual correct data update -
# Miejscowosc depends on RodzajMiejscowosci and so on. If file would
# be updated in other order, foreign keys dependencies will be broken.
fn_dict = OrderedDict([
            ('WMRODZ', RodzajMiejscowosci),
            ('TERC', JednostkaAdministracyjna),
            ('SIMC', Miejscowosc),
            ('ULIC', Ulica),
        ])

# example filename 
fn_regexp = re.compile(r'(?P<model>SIMC|TERC|ULIC|WMRODZ)(_(?P<type>[A-Za-z]+))?(_(?P<date>\d{4}\-\d{2}\-\d{2}))?\.(?P<extension>xml|XML|zip|ZIP)')

url_tmpl = 'http://www.stat.gov.pl/broker/access/'\
            'prefile/downloadPreFile.jspa?id={}'

def match_file_name_to_model_name(file_name):
    match = fn_regexp.match(file_name)
    if match:
        return match.group('model')
    return None

def sort_file_names(file_names):
    # XXX: fn_dict is orderd
    keys = fn_dict.keys()
    file_name_list = [x for x in file_names if match_file_name_to_model_name(os.path.basename(x))]
    return sorted(file_name_list, key=lambda x: keys.index(match_file_name_to_model_name(os.path.basename(x))))



def open_zipfile_from_url(filename, url):
    request = requests.get(url, stream=True)
    zfile = zipfile.ZipFile(io.BytesIO(request.content))
    return zfile


def get_zip_files():
    zip_files = []
    xml_dictionary = get_xml_id_dictionary()
    for file in fn_dict.keys():
        zfile = open_zipfile_from_url(
                file,
                url_tmpl.format(xml_dictionary[file])
            )
        zip_files.append(zfile)

    return zip_files


def update_database(xml_stream, fname, force_flag):
    try:
        teryt_class = fn_dict[match_file_name_to_model_name(os.path.basename(fname))]
    except KeyError as e:
        raise CommandError('Unknown filename: {}'.format(fname))

    try:
        with transaction.atomic():
            teryt_class.objects.all().update(aktywny=False)

            row_list = parse(xml_stream)
            # MySQL doesn't support deferred checking of foreign key
            # constraints. As a workaround we sort data placing rows
            # with no a parent row at the begining.
            if teryt_class is Miejscowosc:
                row_list = sorted(row_list, key=lambda x: '0000000'
                                  if x['SYM'] == x['SYMPOD']
                                  else x['SYM'])

            for vals in row_list:
                instance = teryt_class()
                instance.set_val(vals)
                instance.aktywny = True
                instance.save(force_insert=force_flag)

    except IntegrityError as e:
        raise CommandError("Database integrity error: {}".format(e))
    except DatabaseError as e:
        raise CommandError("General database error: {}\n"
                           "Make sure you run syncdb or migrate before"
                           "importing data!".format(e))
    except TypeError as e:
        raise CommandError("File type error: {}\n"
                           "Check if your file is correct "
                           "xml file".format(e))
