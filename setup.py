import setuptools

print(setuptools.find_packages())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='oss_ar',
     version='0.134',
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
     include_package_data=True,  # for CSV y JSON files
     packages=['oss_ar'],  # setuptools.find_packages(),

     classifiers=[
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
         'Intended Audience :: Developers',
     ],
     python_requires='>=3.6',
)
