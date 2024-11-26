"""
Obtener la lista de obras sociales argentinas desde SSSalud
Grabarla como recurso estático y actualizarla cuando se lo desee
"""
import requests
import json
import csv
import os
import logging
logger = logging.getLogger(__name__)


class ObrasSocialesSSS:

    SERVICE_URL = 'https://www.sssalud.gob.ar/descargas/dump.php'
    # los tipos van de 1 en adelante, no sabemos bien que significa todavia
    params = {'obj': 'listRnosc', 'tipo': 0}
    tipos = {
        "1": "Agentes del Seguro que aceptan Personal de Servicio Doméstico",
        "2": "Obras Sociales para Empleados de Monotributistas",
        "3": "Agentes del Seguro que aceptan de Monotributistas",
        "4": "Agentes del Seguro con Regimen de Adherentes",
        "5": "Agentes del Seguro que aceptan Jubilados y Pensionados",
        "6": "Agentes del Seguro de otra Naturaleza",
        "7": "Agentes del Seguro Sindicales",
        "8": "Agentes del Seguro Estatales",
        "9": "Agentes del Seguro por Convenio",
        "10": "Agentes del Seguro para el Personal de Dirección",
        "11": "Agentes del Seguro de Administración Mixta",
        "12": "Asociaciones de Obras Sociales (A.D.O.S.)",
        "13": "Agentes del Seguro Ley 21.476",
        "14": "Agentes del Seguro de Empresas",
        "15": "Federaciones (Vacio)",
        "16": "Mutuales",
        "17": "Agentes del Seguro Universitarios",
        "18": "Agentes del Seguro por Adhesión",
        "19": "Agentes del Seguro Ley 23.660, Art.1°, inc. i)"
    }

    user_agent = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    )

    here = os.path.dirname(os.path.realpath(__file__))
    base_folder = os.path.join(here, 'data')
    # they use XLS extension but it's a TSV file
    local_excel = os.path.join(base_folder, 'sss-{tipo}.tsv')  # son 19 CSVs
    local_json = os.path.join(base_folder, 'sss.json')  # se pasan a un JSON global
    local_json_object = {}
    # requests records
    raw_response = None
    status_response = None
    errors = []

    processed = False  # ready to use

    def get_oss(self, rnos):
        if not self.processed:
            ret = self.download_databases()
            if not ret:
                return None
            ret = self.process_database()

            return self.local_json_object.get(rnos, {})

    def download_databases(self, force=False):
        # download all databases
        logger.info('Downloading ALL SSS databases')
        oks = 0
        for tipo in self.tipos.keys():
            ret = self.download_database(tipo_obra_social=tipo, force_download=force)
            if ret:
                oks += 1

        return oks > 10  # ponele

    def download_database(self, force_download=False, tipo_obra_social=7):
        """ Download and save database. Return True if OK or None if fails 
            If the file exist we do not re-download. 
            Use force_download for change this behaviour
        """

        logger.info(f'Downloading SSS database tipo {tipo_obra_social}')

        excel_path = self.local_excel.format(tipo=tipo_obra_social)
        if not force_download and os.path.isfile(excel_path):
            return True

        headers = {'User-Agent': self.user_agent}
        self.params['tipo'] = tipo_obra_social
        try:
            response = requests.post(self.SERVICE_URL, data=self.params, headers=headers)
        except Exception as e:
            error = f'Error POST SSSalud: {e}'
            self.errors.append(error)
            self.raw_response = response.content
            self.status_response = response.status_code

            logger.error('{} status:{}'.fomrat(error, self.status_response))

            return None

        self.status_response = response.status_code
        self.raw_response = response.content
        logger.info('respuesta de PUCO: {} {}'.format(response.status_code, response.content))

        # El contenido tiene encoding 'iso-8859-1'
        f = open(excel_path, 'wb')
        f.write(response.content)
        f.close()

        return True

    def process_database(self, force=False):
        """ read the excel file, clean an return/write a nice json file """

        if not force and os.path.isfile(self.local_json):
            f = open(self.local_json, 'r')
            self.local_json_object = json.load(f)
            f.close
            return self.local_json_object

        fieldnames = [
                'rnos', 'denominacion', 'sigla', 'domicilio',
                'localidad', 'cp', 'provincia', 'telefono',
                'otros_telefonos', 'e_mail', 'web'
            ]

        real_rows = {}

        for tipo in self.tipos.keys():
            excel_path = self.local_excel.format(tipo=tipo)
            f = open(excel_path, encoding='ISO-8859-1')
            # the file has 3 bad rows at start
            next(f)  # NEVER
            next(f)  # PUT
            next(f)  # BLANK LINES AT CSVs

            # the headers are bad. e.g. _web_ is at _otros_telefonos_
            reader = csv.DictReader(f, delimiter='\t', fieldnames=fieldnames)

            for row in reader:
                # FIX THE SHIT
                row['web'] = row.get('otros_telefonos', '')
                if type(row['web']) == str:
                    row['web'] = row['web'].strip()

                row['e_mail'] = row.get('telefono', '')
                if type(row['e_mail']) == str:
                    row['e_mail'] = row['e_mail'].strip()

                row['telefono'] = row.get('provincia', '')
                if type(row['telefono']) == str:
                    row['telefono'] = row['telefono'].strip()

                row['provincia'] = row.get('cp', '')
                if type(row['provincia']) == str:
                    row['provincia'] = row['provincia'].strip()

                row['cp'] = row.get('localidad', '')
                if type(row['web']) == str:
                    row['cp'] = row['cp'].strip()

                row['localidad'] = ''
                row['otros_telefonos'] = ''

                row['rnos'] = row['rnos'].strip()
                rnos = row['rnos']
                row['denominacion'] = row['denominacion'].strip()
                row['sigla'] = row['sigla'].strip()
                row['domicilio'] = row['domicilio'].strip()

                new_row = {}
                for k, v in row.items():
                    if v not in [None, '']:  # valor feo como nulo
                        new_row[k] = v

                if rnos not in real_rows:
                    if rnos != 'rnos':
                        real_rows[rnos] = new_row
                else:
                    # DUPLICATED ERROR!
                    self.errors.append(f'Duplicated RNOS: {rnos}')

            f.close()

        f2 = open(self.local_json, 'w')
        f2.write(json.dumps(real_rows, indent=2))
        f2.close

        self.local_json_object = real_rows
        self.processed = True
        return real_rows

    def count_by_province(self):
        """ conut by province """
        ret = {}

        for rnos, oss in self.local_json_object.items():
            provincia = oss['provincia']
            if provincia not in ret:
                ret[provincia] = 0
            ret[provincia] += 1

        return ret
