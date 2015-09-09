#!/usr/bin/env python
from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'requirements.txt')) as f:
    requires = list(filter(lambda x: len(x) > 0, [x.strip() for x in f.read().split('\n')]))

setup(
    name='kanboard-imap',

    version='0.0.0',

    description='Add tasks to a Kanboard server from an IMAP mailbox',

    url='https://github.com/insertjokehere/kanboard-imap',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='kanban kanboard imap',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=requires,

    entry_points={
        'console_scripts': [
            'kanboard_imap=kanboard_imap:main',
        ],
    },
)
