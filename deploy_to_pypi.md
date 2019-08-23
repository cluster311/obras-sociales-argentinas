
# Instalar librerías
pip install --upgrade pip setuptools wheel
pip install tqdm
pip install --user --upgrade twine

# Crear el setup.py

```python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='oss_ar',
     version='0.102',
     license='MIT',
     author="Andres Vazquez",
     author_email="andres@data99.com.ar",
     description="Lista de Obras Sociales Argentinas",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/cluster311/obras-sociales-argentinas",
     install_requires=[
        'requests>2',
     ],
     # package_dir={'': 'src'},
     packages=setuptools.find_packages(),
     classifiers=[
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
         'Intended Audience :: Developers', 
     ],
     python_requires='>=3.6',
 )
```

# Compilar
python3 setup.py bdist_wheel

# Instalar localmente
pip install dist/oss_ar-VERSION-py3-none-any.whl

# Subir a Pypi
python3 -m twine upload dist/oss_ar-VERSION-py3-none-any.whl
