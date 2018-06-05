"""
compiler.py- this module attempts to bring a python script
along with it's data.
"""


__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'
__version__ = '0.0a'

try:
    from archive_data import ArchiveHandler

except ImportError:
    from .archive_data import ArchiveHandler

SCRIPT_SKELETON = '''

{upper_code}

from zipfile import ZipFile
from tarfile import TarFile
import os

_PYTHON_INSTALL_ARCHIVE_FORMAT = '{format}'

_PYTHON_INSTALL_ARCHIVE_OBJECT = TarFile if _PYTHON_INSTALL_ARCHIVE_FORMAT == 'tar' else ZipFile

_PYTHON_INSTALL_DATA_BIN = {archive_data}
with open('~archive.tmp', 'wb') as f:
    f.write(DATA_BIN)

_PYTHON_INSTALL_ARCHIVE_OBJECT('~archive.tmp').extractall()
os.remove('~archive.tmp')

{lower_code}

'''


class ScriptCompiler:
    def __init__(self, script, data):
        self.script = script
        self.data = data

    def get_data(self, upper_code=''):
        dictionary = {
            'format': self.data.archive_type,
            'archive_data': self.data.get_binary_data(),
            'upper_code': upper_code,
            'lower_code': self.script,
        }
        code = SCRIPT_SKELETON.format(**dictionary)
        print(code)


if __name__ == '__main__':
    ScriptCompiler(open('archive_data.py').read(), ArchiveHandler('test-dir')).get_data()
