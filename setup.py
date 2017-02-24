from setuptools import setup, find_packages

setup(
    name='osm_xapi',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/mickael-grima/osm_xapi',
    license='Apache License',
    author='Mickael',
    author_email='mickael.grima@tum.de',
    description='Python package for calling the osm (Open Street Map) xapi (read-only api which returns more data than the normal api)',
    long_description=open("README.md").read(),
    install_requires=[

    ]
)
