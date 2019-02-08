#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
import codecs
import os
import re

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'datagen', '__init__.py')

rel = lambda *args: os.path.join(ROOT, 'src', 'requirements', *args)

_version_re = re.compile(r'__version__\s+=\s+(.*)')
_name_re = re.compile(r'NAME\s+=\s+(.*)')

with open(init, 'rb') as f:
    content = f.read().decode('utf-8')
    version = str(ast.literal_eval(_version_re.search(content).group(1)))
    name = str(ast.literal_eval(_name_re.search(content).group(1)))

readme = codecs.open('README.md').read()

setup(name=name,
      version=version,
      long_description=readme,
      author='Stefano Apostolico',
      author_email='s.apostolico@gmail.com',
      url='https://github.com/unicef/rapidpro-datagen',
      package_dir={'': 'src'},
      install_requires=['click'],
      packages=find_packages('src'),
      include_package_data=True,
      extras_require={'test': ['factory-boy==2.11.1'],
                      },
      entry_points={
          'console_scripts': [
              'generate = datagen.cli:main',
          ],
      },
      license='MIT',
      zip_safe=False,
      keywords='',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Framework :: Django',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.6'
      ])
