# -*- coding: UTF-8 -*-

import glob
import openpyxl
import xmlrpc.client
import config
from xml_rpc_transport_request import RequestsTransport

# Configuraciones
settings = config.settings
# Ficheros xlsx a importar
xlsx_files = glob.glob("f/*.xlsx")

# Capa de transporte para soportar pasar el proxy
transport = RequestsTransport()
common = xmlrpc.client.ServerProxy('{}xmlrpc/2/common'.format(settings.get('url')), transport=transport)
# UID necesario para acceso
uid = common.authenticate(settings.get('db'), settings.get('username'), settings.get('password'), {})
models = xmlrpc.client.ServerProxy('{}xmlrpc/2/object'.format(settings.get('url')), transport=transport)

for file in xlsx_files:
    if '~$' not in file:
        doc = openpyxl.load_workbook(file)
        sheet = doc.worksheets[0]
        sheet_values = list(sheet.values)

        line = 1
        for line in range(1, len(sheet_values)):
            # admin.table.asociado
            print("reading line: %d" % line)
            line += 1
            if len(sheet_values[line]):
                _code = str(sheet_values[line][0]).strip()
                p_name = str(sheet_values[line][4]).strip()
                if not p_name or p_name == 'None':
                    continue
                # Buscar asociado por el codigo
                partner_id = models.execute_kw(settings.get('db'), uid, settings.get('password'),
                                               'res.partner', 'search',
                                               [[['ref', '=', _code]]],
                                               {'limit': 1, 'order': 'id'})
                if partner_id:
                    mobile = str(sheet_values[line][7]).strip()
                    email = str(sheet_values[line][6]).strip()
                    function = str(sheet_values[line][5]).strip()
                    contact_id = models.execute_kw(settings.get('db'), uid, settings.get('password'),
                                                    'res.partner',
                                                    'create',
                                                    [{
                                                       'active': True,
                                                       'parent_id': partner_id[0],
                                                        'name': p_name,
                                                        'mobile': mobile if 'None' != mobile and mobile else False,
                                                        'email': email if 'None' != email and email else False,
                                                        'function': function if 'None' != function and function else False,
                                                        'type': 'contact',
                                                    }]
                                                    )

                    print("contacto creado: %s padre id: %s ref %s" % (str(sheet_values[line][4]).strip(), partner_id[0], _code))
            else:
                break
