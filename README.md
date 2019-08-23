# Obras sociales argentinas
Lista de las obras sociales argentinas

La lista oficial de obras sociales argentinas puede obtenerse por dos vías:
 - Desde el [sitio web de la superintendencia de sistemas de salud](https://www.sssalud.gob.ar/?page=listRnosc&tipo=7) (SSSalud)
 - Desde la página de [SISA](https://sisa.msal.gov.ar/sisa/#sisa) 

Estas listas son diferentes y tienen alrededor de 300 elementos. No cambia mucho al parecer.  

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
Obras sociales encontradas: 214
Errors: []
X provincia: {'TUCUMAN': 3, 'BUENOS AIRES': 18, 'CAPITAL FEDERAL': 155, 'MENDOZA': 4, 'CHUBUT': 2, 'NEUQUEN': 1, 'SANTA FE': 11, 'ENTRE RIOS': 3, 'RIO NEGRO': 1, 'CORDOBA': 10, 'JUJUY': 2, 'NO IDENTIFICADA': 1, 'SANTIAGO DEL ESTERO': 1, 'SALTA': 1, 'CHACO': 1}

```

## Descarga automatizada

Desde SSSalud: Hacer un post a https://www.sssalud.gob.ar/ con los parámetros:  
`{'obj': 'listRnosc', 'tipo': 7}`

Desde SISA se requiere un scpae un poco más complejo.  


