#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
    "ecdsa>=0.15",
    "base58>=2.0.0",
    "pyyaml>=5.1",
    "cashaddress>=1.0.6",
]

setup(
    name='btc-address-dump',
    version='0.3.2',
    author='cig01',
    url='https://github.com/10gic/btc-address-dump',
    license='MIT License',
    description='A utility for dump btc address from mnemonic words or private key or public key',
    long_description=open('README.rst').read(),
    install_requires=["ecdsa>=0.15", "base58>=2.0.0", "pyyaml>=5.1", "cashaddress>=1.0.6"],
    python_requires='>=3',
    packages=['btc_address_dump'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    platforms='any',
    entry_points={'console_scripts': ['btc_address_dump=btc_address_dump:run_main']})
