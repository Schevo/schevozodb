__version__ = '3.1a1'

from setuptools import setup, Extension, find_packages
import sys, os
import textwrap


setup(
    name="SchevoZodb",

    version=__version__,

    description="ZODB3 storage backend for Schevo",

    long_description=textwrap.dedent("""
    SchevoZodb provides integration between the ZODB3_ object database
    for Python and the Schevo_ DBMS.

    The latest development version is available in a `Subversion
    repository <http://schevo.org/svn/trunk/Zodb#egg=SchevoZodb-dev>`__.

    .. _Schevo: http://schevo.org/
    
    .. _ZODB3: http://www.zope.org/Products/ZODB3
    """),

    classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Database :: Database Engines/Servers',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],

    keywords='database dbms',

    author='Orbtech, L.L.C. and contributors',
    author_email='schevo@googlegroups.com',

    url='http://schevo.org/wiki/SchevoZodb',

    license='LGPL',

    platforms=['UNIX', 'Windows'],

    packages=find_packages(exclude=['doc', 'tests']),

    include_package_data=True,

    zip_safe=False,

    install_requires=[
    'Schevo == dev, >= 3.1a1dev-r3555',
    'ZODB3 >= 3.8.0b3',
    ],

    tests_require=[
    'nose >= 0.9.0',
    ],
    test_suite='nose.collector',

    extras_require={
    },

    dependency_links = [
    'http://schevo.org/files/thirdparty/',
    ],

    entry_points = """
    [schevo.backend]
    zodb = schevozodb.backend:ZodbBackend
    """,
    )
