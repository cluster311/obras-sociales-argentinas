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
    params = {'obj': 'listRnosc', 'tipo': 7}
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    
    here = os.path.dirname(os.path.realpath(__file__))
    base_folder = os.path.join(here, 'data')
    # they use XLS extension but it's a TSV file
    local_excel = os.path.join(base_folder, 'sss-{tipo}.tsv')  # son 18 CSVs
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

    def download_databases(self):
        # download all databases
        logger.info(f'Downloading ALL SSS databases')
        oks = 0
        for tipo in range(1, 19):
            ret = self.download_database(tipo_obra_social=tipo)
            if ret:
                oks += 1
        
        return oks > 10  # ponele

    def download_database(self, force_download=False, tipo_obra_social=7):
        """ Download and save database. Return True if OK or None if fails 
            If the file exist we do not re-download. 
            Use force_download for change this behaviour """
        
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

        f = open(excel_path, 'wb')
        f.write(response.content)
        f.close()

        """ no hace falta al parecer
        # encode_to = 'utf-8'
        encode_to = 'iso-8859-1'
        data = response.content.decode(encode_to)
        f = open('sss2.xls', 'w')
        f.write(data)
        f.close()
        """

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

        for tipo in range(1, 19):
            excel_path = self.local_excel.format(tipo=tipo)
            f = open(excel_path, encoding='ISO-8859-1')
            # the file has 3 bad rows at start
            next(f)  # NEVER
            next(f)  #   PUT 
            next(f)  #     BLANK LINES AT CSVs
            
            # the headers are bad. e.g. _web_ is at _otros_telefonos_
            
            reader = csv.DictReader(f, delimiter='\t', fieldnames=fieldnames)
            
            errors = []
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
