from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import DBNormalizer

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.txt', 'CHANGES.txt')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='DBNormalizer',
    version=DBNormalizer.__version__,
    url='http://github.com/humbertog/DBNormalizer/',
    author=['Gabriela', 'Maria', 'Humberto', 'Harsha', 'Bishnu'],
    tests_require=['pytest'],
    install_requires=[ 'SQLalchemy>=0.8.2'],
    cmdclass={'test': PyTest},
    author_email='humberto_gora@gmail.com,gabrielahrlr@gmail.com',
    description='Data base normalizer',
    long_description=long_description,
    packages=['DBNormalizer/controller', 'DBNormalizer/model', 'DBNormalizer/view'],
    include_package_data=True,
    platforms='any',
    test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Beta'
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
