from setuptools import setup, find_packages
import os

version = '0.2.1'

setup(name='socialapps.dmessages',
      version=version,
      description="In-site direct messaging system",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='iServices de Mexico',
      author_email='desarrollo@iservices.com.mx',
      url='http://iservices.com.mx/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['socialapps'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'socialapps.core',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
