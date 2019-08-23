"""
Integrate all resources
"""
from oss_ar.sssalud import ObrasSocialesSSS
from oss_ar.sisa import ObrasSocialesSISA


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
