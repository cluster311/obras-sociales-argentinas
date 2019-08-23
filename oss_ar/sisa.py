"""
Obtener la lista de obras sociales argentinas desde SISA
Grabarla como recurso estático y actualizarla cuando se lo desee

Scrape complicado
Desde la página de [SISA](https://sisa.msal.gov.ar/sisa/#sisa) accediendo a:

Reportes -> 
    Codificaciones auxiliares -> 
        Codificaciones Compartidas ->
            Coberturas sociales ->
                Se abre la tabla
                -> En el boton de config de la tabla, elegir todos los campos
                -> Link de descarga en la parte inferior de la tabla

"""
import requests
import json
import csv
import os
import logging
logger = logging.getLogger(__name__)


class ObrasSocialesSISA:

    SERVICE_URL = None
    params = {}
    user_agent = ''
    
    base_folder = dir_path = os.path.dirname(os.path.realpath(__file__))
    local_csv = os.path.join(base_folder, 'sisa.csv')
    local_json = os.path.join(base_folder, 'sisa.json')
    local_json_object = {}
    # requests records
    raw_response = None
    status_response = None
    errors = []

    processed = False  # ready to use

    def get_oss(self, rnos):
        if not self.processed:
            ret = self.download_database()
            if not ret:
                return None
            ret = self.process_database()

            return self.local_json_object.get(rnos, {})

    def download_database(self, force_download=False):
        """ Scrape needed. We use static download """
        
        return True
    
    def process_database(self, force=False):
        """ read the CSV file, clean an return/write a nice json file """
        if not force and os.path.isfile(self.local_json):
            f = open(self.local_json, 'r')
            self.local_json_object = json.load(f)
            f.close
            return self.local_json_object

        f = open(self.local_csv)
        
        # the headers are bad. e.g. _web_ is at _otros_telefonos_
        fieldnames = [
                'Código', 'RNOS', 'Nombre', 'Tipo de cobertura',
                'Provincia', 'Localidad','Sigla', 'Domicilio',
                'Teléfono 1', 'Teléfono 2', 'Mail'
                ]
        reader = csv.DictReader(f, fieldnames=fieldnames)
        real_rows = {}
        errors = []
        for row in reader:
            rnos = row.get('RNOS', row.get('Código', ''))
            new_row = {}
            for k, v in row.items():
                if v not in [None, 'null']:  # valor feo como nulo
                    new_row[k] = v

            if rnos not in real_rows:
                if rnos != 'RNOS':
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
            provincia = oss['Provincia']
            if provincia not in ret:
                ret[provincia] = 0
            ret[provincia] += 1

        return ret
