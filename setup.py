# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from Cython.Build import cythonize


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ews',
    version='0.1.0',
    description='Early-warning signals for python',
    long_description=readme,
    author='Tobias Brett',
    author_email='tobybrett@gmail.com',
    url='https://github.com/tsbrett/py_earlywarnings',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    ext_modules = cythonize("ews/kolmogorov_complexity.pyx")
)

