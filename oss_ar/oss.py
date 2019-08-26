"""
Integrate all resources
"""
from oss_ar.sssalud import ObrasSocialesSSS
from oss_ar.sisa import ObrasSocialesSISA
import json
import os
import logging
logger = logging.getLogger(__name__)


class ObraSocialArgentina:
    """ cada una de las obras sociales
        Descarga todo los necesario para procesar """

    rnos = None
    exists = False
    nombre = None
    tipo_de_cobertura = None
    sigla = None
    provincia = None
    localidad = None
    domicilio = None
    cp = None
    telefonos = set()
    emails = set()
    web = None

    def __init__(self, rnos):
        self.rnos = rnos

        sisa = ObrasSocialesSISA()
        oss_sisa = sisa.get_oss(rnos=rnos)

        sss = ObrasSocialesSSS()
        oss_sss = sss.get_oss(rnos=rnos)

        if oss_sisa == oss_sss == {}:
            return
        self.exists = True

        # mezclar ambos
        self.nombre = oss_sisa.get('Nombre', oss_sss.get('denominacion', 'OSS SIN NOMBRE'))
        self.tipo_de_cobertura = oss_sisa.get('Tipo de cobertura', '')
        self.sigla = oss_sisa.get('Sigla', oss_sss.get('sigla', ''))
        self.provincia = oss_sisa.get('Provincia', oss_sss.get('provincia', ''))
        self.localidad = oss_sisa.get('Localidad', oss_sss.get('localidad', ''))
        self.domicilio = oss_sisa.get('Domicilio', oss_sss.get('domicilio', ''))
        self.cp = oss_sss.get('cp', '')
        self.telefonos = set()
        self.emails = set()
        
        telefonos = [oss_sisa.get('Teléfono 1', None),
                     oss_sisa.get('Teléfono 2', None),
                     oss_sss.get('telefono', None),
                     oss_sss.get('otros_telefonos', None)
                     ]
        for tel in telefonos:
            if tel is not None:
                self.telefonos.add(tel)
        
        email1 = oss_sisa.get('Mail', None)
        email2 = oss_sss.get('e_mail', None)
        if email1 is not None:
            self.emails.add(email1)
        if email2 is not None:
            self.emails.add(email2)

        self.web = oss_sss.get('web', None)
    
    def as_dict(self):
        dct = {
            'rnos': self.rnos,
            'exists': self.exists,
        }
        if self.exists:
            dct.update({
                'nombre': self.nombre,
                'tipo_de_cobertura': self.tipo_de_cobertura,
                'sigla': self.sigla,
                'provincia': self.provincia,
                'localidad': self.localidad,
                'domicilio': self.domicilio,
                'cp': self.cp,
                'telefonos': list(self.telefonos),  # set no es serializable (?)
                'emails': list(self.emails),
                'web': self.web
            })
        return dct


class ObrasSocialesArgentinas:
    """ clase singleton que te devuelve toda la lista de obras sociales"""

    here = os.path.dirname(os.path.realpath(__file__))
    base_folder = os.path.join(here, 'data')
    # they use XLS extension but it's a TSV file
    local_json = os.path.join(base_folder, 'final-oss.json')  # se pasan a un JSON global
    local_json_object = {}  # todas las obras sociales mezcladas de los origenes

    processed = False  # ready for use

    def __init__(self):
        
        self.process_database()  # initialice databases
    
    def process_database(self, force=False):
        """ read the excel file, clean an return/write a nice json file """

        if not force and os.path.isfile(self.local_json):
            f = open(self.local_json, 'r')
            self.local_json_object = json.load(f)
            f.close
            self.processed = True
            return self.local_json_object
        
        logger.info('Merging databases')
        sisa = ObrasSocialesSISA()
        sss = ObrasSocialesSSS()
        
        sisa.process_database()
        sss.process_database()
        
        real_rows = {}

        for rnos, oss in sisa.local_json_object.items():
            # en SISA esta el "PLAN NACER/PROGRAMA SUMAR" que tiene _Código_ pero no RNOS (?)
            rnos = oss.get('RNOS', oss.get('Código'))
            # mezclar los dos origenes
            osa = ObraSocialArgentina(rnos=rnos)
            # agregar al dict final
            real_rows[rnos] = osa.as_dict()
            real_rows[rnos]['sources'] = ['SISA']
            # limpiar el de SSSalud para iterar despues si quedó alguno
            oss_sss = sss.local_json_object.get(rnos, {})
            exists_at_oss = oss_sss != {}
            if exists_at_oss:
                sss.local_json_object[rnos]['processed'] = True
                real_rows[rnos]['sources'].append('SSSalud')

        # procesar los que faltan en SSS
        for rnos, oss in sss.local_json_object.items():
            if 'processed' in oss:
                continue
            osa = ObraSocialArgentina(rnos=rnos)
            # agregar al dict final
            real_rows[rnos] = osa.as_dict()
            real_rows[rnos]['sources'] = ['SSSalud']
        
        f2 = open(self.local_json, 'w')
        f2.write(json.dumps(real_rows, indent=2))
        f2.close

        self.local_json_object = real_rows
        self.processed = True
        return real_rows

    def search(self, txt):
        if not self.processed:
            self.process_database()

        for rnos, oss in self.local_json_object.items():
            # saca del medio, Solr
            full_str = ' '.join([str(val).lower() for key, val in oss.items()])
            if full_str.find(txt.lower()) > -1:
                yield oss
