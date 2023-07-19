import os
from setuptools import setup, find_packages
from codecs import open

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ezgpx',
    version='0.1.3',
    description='Easy to use Python GPX library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['gpx', 'gpx-files', 'gpx-parser', 'gpx-reader', 'gpx-writer', 'gpx-data'],
    url='https://pypi.org/project/ezgpx/',
    download_url='https://github.com/FABallemand/ezGPX',
    project_urls={
            "Bug Tracker": "https://github.com/FABallemand/ezGPX/issues",
            "Documentation": "https://ezgpx.readthedocs.io/en/latest/",
            "Source Code": "https://github.com/FABallemand/ezGPX",
        },
    author='Fabien ALLEMAND',
    author_email='allemand.fabien@orange.fr',
    license='GNU GPLv3',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['gmap', 'folium'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)