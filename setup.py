import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGES')).read()

requires = [
    'cx_oracle',
    'giblets',
    'pyodbc',
    'Sphinx',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    ]
tests_require = ['nose', 'coverage', ]

setup(name='CRM2MSTR',
      version='1.0',
      description='CRM2MSTR',
      long_description = README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        ],
      author='Lee Doolan',
      author_email='ldoolan@paradigm-healthcare.com',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='crm2mstr',
      install_requires=requires,
      )

