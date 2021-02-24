#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

import os
from setuptools import find_packages, setup
from pympristui import __version__, app_desc

def readme():
    with open('README.md') as f:
        return f.read()

app_name = 'pympristui'

setup(
        name=app_name,
        version=__version__,
        license='zlib/libpng',
        description=app_desc,
        long_description=readme(),
        long_description_content_type='text/markdown',
        url='https://github.com/apocalyptech/pympristui',
        author='CJ Kucera',
        author_email='cj@apocalyptech.com',
        data_files=[
            # I always like these to be installed along with the apps
            (f'share/{app_name}', ['COPYING.txt', 'README.md', 'requirements.txt']),
            ],
        install_requires=[
            'dbus-python ~= 1.2, >= 1.2.16',
            'mpris2 ~= 1.0, >= 1.0.2',
            'urwid ~= 2.1, >= 2.1.2',
            ],
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console :: Curses',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: zlib/libpng License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Topic :: Multimedia :: Sound/Audio',
            'Topic :: Utilities',
            ],
        scripts=[
            'pympristui.py',
            ],
        )

