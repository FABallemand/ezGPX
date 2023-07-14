import os
from setuptools import setup, find_packages
from codecs import open

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ezGPX',
    version='0.1.0',
    description='Easy to use Python GPX library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    # url='https://medium-multiply.readthedocs.io/',
    author='Fabien ALLEMAND',
    author_email='allemand.fabien@orange.fr',
    license='GNU GPLv3',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent'
    ],
    packages=find_packages(include=['ezgpx']),
    include_package_data=True,
    install_requires=["gmap", "folium"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)

# setup(
#     name='ezGPX',
#     # packages=find_packages(include=['mypythonlib']),
#     packages=find_packages(),
#     version='0.1.0',
#     description='Easy to use Python GPX library',
#     author='Fabien ALLEMAND',
#     license='GNU GPLv3',
#     install_requires=[],
#     setup_requires=['pytest-runner'],
#     tests_require=['pytest'],
#     test_suite='tests',
# )