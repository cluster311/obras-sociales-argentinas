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
    
    # they use XLS extension but it's a TSV file
    local_excel = 'sss.tsv'  # Path
    local_json = 'sss.json'  # path
    local_json_object = None
    # requests records
    raw_response = None
    status_response = None
    errors = []

    def download_database(self, force_download=False):
        """ Download and save database. Return True if OK or None if fails 
            If the file exist we do not re-download. 
            Use force_download for change this behaviour """
        if not force_download and os.path.isfile(self.local_excel):
            return True

        headers = {'User-Agent': self.user_agent}
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

        f = open(self.local_excel, 'wb')
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
    
    def process_database(self):
        """ read the excel file, clean an return/write a nice json file """

        # the file has 3 bad rows at start
        
        f = open(self.local_excel, encoding='ISO-8859-1')
        
        next(f)  # NEVER
        next(f)  #   PUT 
        next(f)  #     BLANK LINES AT CSVs
        
        # the headers are bad. e.g. _web_ is at _otros_telefonos_
        fieldnames = [
            'rnos', 'denominacion', 'sigla', 'domicilio',
            'localidad', 'cp', 'provincia', 'telefono',
            'otros_telefonos', 'e_mail', 'web'
        ]
        reader = csv.DictReader(f, delimiter='\t', fieldnames=fieldnames)
        real_rows = {}
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

            if rnos not in real_rows:
                if rnos != 'rnos':
                    real_rows[rnos] = row
            else:
                # DUPLICATED ERROR!
                self.errors.append(f'Duplicated RNOS: {rnos}')
        
        f.close()
        f2 = open(self.local_json, 'w')
        f2.write(json.dumps(real_rows, indent=2))
        f2.close

        self.local_json_object = real_rows
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
        

if __name__ == '__main__':
    s = ObrasSocialesSSS()
    s.download_database()
    rows = s.process_database()
    print('Obras sociales encontradas: {}'.format(len(rows.keys())))
    print('Errors: {}'.format(s.errors))
    ret = s.count_by_province()
    print('X provincia: {}'.format(ret))