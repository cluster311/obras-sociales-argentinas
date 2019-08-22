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
    
    # they use XLS extension but it's a TSV file
    local_csv = 'sisa.csv'  # Path
    local_json = 'sisa.json'  # path
    local_json_object = None
    # requests records
    raw_response = None
    status_response = None
    errors = []

    def download_database(self, force_download=False):
        """ Scrape needed. We use static download """
        
        return True
    
    def process_database(self):
        """ read the CSV file, clean an return/write a nice json file """

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
            
            if rnos not in real_rows:
                if rnos != 'RNOS':
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
            provincia = oss['Provincia']
            if provincia not in ret:
                ret[provincia] = 0
            ret[provincia] += 1

        return ret
        

if __name__ == '__main__':
    s = ObrasSocialesSISA()
    s.download_database()
    rows = s.process_database()
    print('Obras sociales encontradas: {}'.format(len(rows.keys())))
    print('Errors: {}'.format(s.errors))
    ret = s.count_by_province()
    print('X provincia: {}'.format(ret))