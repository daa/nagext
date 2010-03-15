#!/usr/bin/python

from distutils.core import setup

setup(name='python-nagext',
    version='0.1',
    description='Python interface to Nagios external commands',
    long_description='This module allows sending external commands to Nagios from Python',
    license='LGPL3',
    author='Alexander Duryagin',
    author_email='daa@vologda.ru',
    url='http://github.com/daa/nagext',
    py_modules=['nagext'])

