from distutils.core import setup
# see http://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
from distutils.command.install import INSTALL_SCHEMES 
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# this hackiness is based on https://wiki.python.org/moin/Distutils/Tutorial
import os, sys, glob, fnmatch

## Added 10 Jan 2008
from distutils.core import setup, Extension
import distutils.command.install_data

## Code borrowed from wxPython's setup and config files
## Thanks to Robin Dunn for the suggestion.
## I am not 100% sure what's going on, but it works!
def opj(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)

def find_data_files(srcdir, *wildcards, **kw):
    # get a list of all files under the srcdir matching wildcards,
    # returned in a format to be used for install_data
    def walk_helper(arg, dirname, files):
        names = []
        lst, wildcards = arg
        for wc in wildcards:
            wc_name = opj(dirname, wc)
            for f in files:
                filename = opj(dirname, f)

                if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                    names.append(filename)
        if names:
            lst.append( (dirname, names ) )

    file_list = []
    recursive = kw.get('recursive', True)
    if recursive:
        os.path.walk(srcdir, walk_helper, (file_list, wildcards))
    else:
        walk_helper((file_list, wildcards),
                    srcdir,
                    [os.path.basename(f) for f in glob.glob(opj(srcdir, '*'))])
    return file_list

files=find_data_files('gae_mini_profiler/static', '*') + find_data_files('gae_mini_profiler/templates', '*')

setup(
    name='gae_mini_profiler',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0',

    description='PIP-supported fork of Khan GAE mini profiler',
    long_description=long_description,
    license='LICENSE.txt',

    # The project's main homepage.
    url='https://github.com/bogdanvarlamov/gae_mini_profiler',

    # Author details
    author='Bogdan Varlamov',
    author_email='bogdanvarlamov@gmail.com',


    packages = ["gae_mini_profiler", "gae_mini_profiler.unformatter", "gae_mini_profiler.test"],

    data_files= files

)
