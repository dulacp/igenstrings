#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'clint',
]

test_requirements = [

]

setup(
    name='igenstrings',
    version='0.1.0',
    description="Enhance the genstrings command by adding merging capabilities",
    long_description=readme + '\n\n' + history,
    author="Pierre Dulac",
    author_email='pierre@dulaccc.me',
    url='https://github.com/dulaccc/igenstrings',
    packages=[
        'igenstrings',
    ],
    package_dir={'igenstrings':
                 'igenstrings'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='igenstrings',
    entry_points={
        'console_scripts': [
            'igenstrings = igenstrings.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
