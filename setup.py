# coding: utf-8

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

description = 'Python framework for multi-asset backtesting.'


setup(
    name='epymetheus',
    version='0.1.0',
    description=description,
    long_description=description,
    long_description_content_type='text/markdown',
    install_requires=requirements,
    author='Shota Imaki',
    author_email='shota.imaki@icloud.com',
    maintainer='Shota Imaki',
    maintainer_email='shota.imaki@icloud.com',
    url='https://github.com/simaki/epymetheus',
    packages=find_packages(include=["epymetheus", "epymetheus.*"]),
    license=license,
    classifiers=[
        'Intended Audience :: Financial and Insurance Industry'
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial :: Investment'
    ]
)
