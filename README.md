# Instalacion

```
pip install oss_ar
```

# Obras sociales argentinas
Lista de las obras sociales argentinas

La lista oficial de obras sociales argentinas puede obtenerse por dos vías:
 - Desde el [sitio web de la superintendencia de sistemas de salud](https://www.sssalud.gob.ar/?page=listRnosc&tipo=7) (SSSalud)
 - Desde la página de [SISA](https://sisa.msal.gov.ar/sisa/#sisa) 

Estas listas son diferentes y tienen alrededor de 300 elementos. Los elementos de la lista no cambian casi nunca. Por eso esta base estática.  
El objeto ObraSocialArgentina es una mezcla terminada de las dos fuentes de datos. Alcanza para un uso general.

```python
from oss_ar.oss import ObraSocialArgentina
import json
rnoss = ['900103', '800501', '117702']
for rnos in rnoss:
    oss = ObraSocialArgentina(rnos=rnos)
    nice_dict = json.dumps(oss.as_dict(), indent=2)
    print(nice_dict)
```

```js
{
  "rnos": "900103",
  "exists": false
}
{
  "rnos": "800501",
  "exists": true,
  "nombre": "OBRA SOCIAL ACEROS PARANA",
  "tipo_de_cobertura": "Obra social",
  "sigla": "",
  "provincia": "Buenos Aires",
  "localidad": "SAN NICOLAS DE LOS ARROYOS",
  "domicilio": "AVDA. MORENO 187",
  "cp": "",
  "telefonos": [
    "03461-43-7600",
    "03461-425632"
  ],
  "emails": [
    "info@osap.org.ar"
  ],
  "web": null
}
{
  "rnos": "117702",
  "exists": true,
  "nombre": "OBRA SOCIAL DEL PERSONAL DE PRENSA DE MAR DEL PLATA",
  "tipo_de_cobertura": "Obra social",
  "sigla": "OSPREN",
  "provincia": "Buenos Aires",
  "localidad": "MAR DEL PLATA  (MAR DEL PLATA)",
  "domicilio": "DORREGO 1734",
  "cp": "7600",
  "telefonos": [
    "03461-43-7600",
    "03461-425632",
    "0223-4-734394"
  ],
  "emails": [
    "info@osap.org.ar",
    "ospren@ospren.org.ar"
  ],
  "web": "www.prensamardelplata.org.ar"
}

```

## Trabajar sobre la lista completa


La lista completa de Obras sociales puede usarse para buscar o trabajar soble la lista completa

```python
from oss_ar.oss import ObrasSocialesArgentinas
osss = ObrasSocialesArgentinas()
# la lista completa esta disponible en _osss.local_json_object_

print(osss.local_json_object['117702'])
```

```
{'rnos': '117702', 'exists': True, 'nombre': 'OBRA SOCIAL DEL PERSONAL DE PRENSA DE MAR DEL PLATA', 'tipo_de_cobertura': 'Obra social', 'sigla': 'OSPREN', 'provincia': 'Buenos Aires', 'localidad': 'MAR DEL PLATA  (MAR DEL PLATA)', 'domicilio': 'DORREGO 1734', 'cp': '7600', 'telefonos': ['0223-4-734394'], 'emails': ['ospren@ospren.org.ar'], 'web': 'www.prensamardelplata.org.ar', 'sources': ['SISA', 'SSSalud']}
```

Buscar obras sociales
```python
# buscar
for resultado in osss.search('mendoza'):
  print(resultado)
```

```
{'rnos': '406', 'exists': True, 'nombre': 'OBRA SOCIAL DEL PERSONAL DEL ORGANISMO DE CONTROL EXTERNO', 'tipo_de_cobertura': 'Obra social', 'sigla': 'OSPOCE', 'provincia': 'CABA', 'localidad': 'CIUDAD DE BUENOS AIRES', 'domicilio': 'BARTOLOME MITRE 1523 PISO 1 B', 'cp': '1037', 'telefonos': ['0800-321-6776(O.S.)', '5510-5000'], 'emails': [], 'web': 'www.ospoce.com.ar', 'sources': ['SISA', 'SSSalud']}
>>> for resultado in osss.search('mendoza'):
...   print(resultado)
... 
{'rnos': '909001', 'exists': True, 'nombre': 'O.S.P. MENDOZA (OSEP)', 'tipo_de_cobertura': 'Obra social', 'sigla': 'OSEP', 'provincia': 'Mendoza', 'localidad': '', 'domicilio': 'Sin especificar', 'cp': '', 'telefonos': [], 'emails': [], 'web': None, 'sources': ['SISA']}
{'rnos': '127000', 'exists': True, 'nombre': 'OBRA SOCIAL DE TRABAJADORES DE ESTACIONES DE SERVICIO', 'tipo_de_cobertura': 'Obra social', 'sigla': 'OSTES', 'provincia': 'Mendoza', 'localidad': 'GUAYMALLEN', 'domicilio': 'BANDERA DE LOS ANDES 239', 'cp': '5521', 'telefonos': ['0261-4326-292', '0261-431-7309'], 'emails': [], 'web': None, 'sources': ['SISA', 'SSSalud']}
{'rnos': '117801', 'exists': True, 'nombre': ' OBRA SOCIAL DEL PERSONAL DE PRENSA DE MENDOZA', 'tipo_de_cobertura': 'Obra social', 'sigla': '', 'provincia': 'Mendoza', 'localidad': 'MENDOZA', 'domicilio': 'CHILE 1661', 'cp': '5500', 'telefonos': ['0261-4-251469', '0261-4-251179'], 'emails': ['prensaludmza@hprensaludmza.org.ar'], 'web': None, 'sources': ['SISA', 'SSSalud']}
{'rnos': '112301', 'exists': True, 'nombre': 'OBRA SOCIAL DEL PERSONAL DE MICROS Y OMNIBUS DE MENDOZA', 'tipo_de_cobertura': 'Obra social', 'sigla': 'OSPEMOM', 'provincia': 'Mendoza', 'localidad': 'MENDOZA', 'domicilio': 'CATAMARCA 382', 'cp': '5500', 'telefonos': ['0261-4-203283', '0261-4-203342'], 'emails': ['ospemom@ospemom.org.ar'], 'web': None, 'sources': ['SISA', 'SSSalud']}
{'rnos': '108506', 'exists': True, 'nombre': 'OBRA SOCIAL DEL PERSONAL DE MANIPULEO, EMPAQUE Y EXPEDICION DE FRUTA FRESCA Y HORTALIZAS DE CUYO', 'tipo_de_cobertura': 'Obra social', 'sigla': 'OSFYHC', 'provincia': 'Mendoza', 'localidad': 'MENDOZA', 'domicilio': 'MONTECASEROS 1147', 'cp': '5500', 'telefonos': ['0261-423-8440', '0261-4-299591'], 'emails': [], 'web': 'EN CRISIS CONFORME DECRETO 1400/01 - (VER OBSERVAC', 'sources': ['SISA', 'SSSalud']}
{'rnos': '2303', 'exists': True, 'nombre': 'OBRA SOCIAL PARA EL PERSONAL DE EMPRESAS DE LIMPIEZA, SERVICIOS Y MAESTRANZA DE MENDOZA', 'tipo_de_cobertura': 'Obra social', 'sigla': '', 'provincia': 'Mendoza', 'localidad': 'MENDOZA', 'domicilio': 'SAN LORENZO 221', 'cp': '5500', 'telefonos': ['0800-666-5579', '0261-420-1638'], 'emails': ['ospelsym@ospelsym.com.ar'], 'web': 'www.ospelsym.com.ar', 'sources': ['SISA', 'SSSalud']}
{'rnos': '703', 'exists': True, 'nombre': 'MUTUAL DEL PERSONAL DEL AGUA Y LA ENERGIA DE MENDOZA', 'tipo_de_cobertura': 'Obra social', 'sigla': '', 'provincia': 'Mendoza', 'localidad': 'MENDOZA', 'domicilio': 'JOSE VICENTE ZAPATA 144', 'cp': '5500', 'telefonos': ['0261-4292012'], 'emails': ['mutualaye@infovia.com.ar'], 'web': None, 'sources': ['SISA', 'SSSalud']}

```

```python
# ver las OSS que estan en la bases de datos de SISA o SSSalud
count = {}
for rnos, oss in osss.local_json_object.items():
  key = '-'.join([val for val in oss['sources']])
  if key not in count:
    count[key] = 0
  count[key] += 1

print(count)
```

```
{'SISA': 44, 'SISA-SSSalud': 288, 'SSSalud': 8}
```

Ver cuales Obras sociales provienen de SSSalud yn no están en SISA
```python
solo_sss = ['{} {}'.format(oss['rnos'], oss['nombre']) for rnos, oss in osss.local_json_object.items() if oss['sources'] == ['SSSalud']]
print('\n\t'.join(solo_sss))
```

```
3702 OBRA SOCIAL  YACIMIENTOS CARBONIFEROS
3801 OBRA SOCIAL  WITCEL
128300 OBRA SOCIAL PEONES DE TAXIS DE ROSARIO
128508 OBRA SOCIAL DE FARMACEUTICOS Y BIOQUIMICOS
128607 OBRA SOCIAL DE TRABAJADORES DEL PETROLEO Y GAS PRIVADO DEL CHUBUT
128706 OBRA SOCIAL DEL PERSONAL DE DRAGADO Y BALIZAMIENTO
128805 OBRA SOCIAL DEL PERSONAL ADUANERO DE LA REPUBLICA ARGENTINA
128904 OBRA SOCIAL DE LOS TRABAJADORES ARGENTINOS DE CENTROS DE CONTACTOS
```

## Funcionamiento interno

Esta librería usa los CSVs de origen de estas dos fuentes y mezcla los datos. Expone tambien las clases internas.

### Según SISA

```python
from oss_ar.sisa import ObrasSocialesSISA
s = ObrasSocialesSISA()
s.download_database()
rows = s.process_database()
print('Obras sociales encontradas: {}'.format(len(rows.keys())))
print('Errors: {}'.format(s.errors))
ret = s.count_by_province()
print('X provincia: {}'.format(ret))
```

```
Obras sociales encontradas: 332
Errors: []
X provincia: {'Ministerio de Salud de la Nación': 2, 'Tierra del Fuego': 1, 'Santa Cruz': 1, 'Río Negro': 2, 'Neuquén': 2, 'Misiones': 2, 'La Pampa': 1, 'Formosa': 2, 'Chubut': 5, 'Chaco': 3, 'Tucumán': 4, 'Santiago del Estero': 2, 'Santa Fe': 21, 'San Luis': 1, 'San Juan': 2, 'Salta': 2, 'Mendoza': 7, 'La Rioja': 1, 'Jujuy': 3, 'Entre Ríos': 6, 'Corrientes': 2, 'Córdoba': 14, 'Catamarca': 1, 'Buenos Aires': 37, 'CABA': 208}
```

### Según SSSalud

```python
from oss_ar.sssalud import ObrasSocialesSSS
s = ObrasSocialesSSS()
s.download_database()
rows = s.process_database()
print('Obras sociales encontradas: {}'.format(len(rows.keys())))
print('Errors: {}'.format(s.errors))
ret = s.count_by_province()
print('X provincia: {}'.format(ret))
```

```
Obras sociales encontradas: 296
Errors: ['Duplicated RNOS: 208', ...]
X provincia: {'CORDOBA': 13, 'BUENOS AIRES': 32, 'CAPITAL FEDERAL': 209, 'MENDOZA': 6, 'SANTA FE': 16, 'JUJUY': 2, 'SALTA': 1, 'TUCUMAN': 3, 'RIO NEGRO': 1, 'SANTIAGO DEL ESTERO': 1, 'ENTRE RIOS': 5, 'CHUBUT': 4, 'CHACO': 1, 'NEUQUEN': 1, 'NO IDENTIFICADA': 1}
```

## Descarga automatizada

Desde SSSalud: Hacer un post a https://www.sssalud.gob.ar/descargas/dump.php con los parámetros:  
`{'obj': 'listRnosc', 'tipo': 7}` (el tipo va del 1 al 18).  

Desde SISA se requiere un scpae un poco más complejo.  


