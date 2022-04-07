# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'kmatch/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


setup(
    name='kmatch',
    version=get_version(),
    description='A language for matching/validating/filtering Python dictionaries',
    long_description=open('README.rst').read(),
    url='https://github.com/ambitioninc/kmatch',
    author='Wes Kendall',
    author_email='opensource@ambition.com',
    keywords='matching, dictionaries, filtering, validation',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
    ],
    license='MIT',
    install_requires=[],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=[
        'nose>=1.3.0',
        'coverage>=3.7.1',
        'mock>=1.0.1',
    ],
    zip_safe=False,
)
