"""The setup script for plsql2postgre."""
import os
import codecs
from   setuptools    import setup
import plsql2postgre

HERE = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """Return multiple read calls to different readable objects as a single string."""
    return codecs.open(os.path.join(HERE, *parts), 'r', encoding='utf-8').read()

LONG_DESCRIPTION = read('README.md')

setup(
    name='plsql2postgre',
    version=plsql2postgre.__version__,
    author='yangyose',
    author_email='yangyose@hotmail.com',
    url='http://github.com/yangyose/plsql2postgre/',
    license='MIT License',
    description='SQL converter from Oracle to PostgreSQL',
    long_description=LONG_DESCRIPTION,
    packages=['plsql2postgre'],
    include_package_data=True,
    scripts=[
        'scripts/pygrun',
        'scripts/antlr4env.bat',
        'scripts/pyanalyzeenv.bat',
        'scripts/venvscript.bat',
    ],
    install_requires=[
        'antlr4-python3-runtime',
    ],
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    zip_safe=False,
)
