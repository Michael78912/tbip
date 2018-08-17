"""
compiler.py- this module attempts to bring a python script
along with it's data.
"""


__author__ = 'Michael Gill <michaelveenstra12@gmail.com>'
__version__ = '0.0a'

import base64
import io

try:
    from archive_data import ArchiveHandler

except ImportError:
    from .archive_data import ArchiveHandler

SCRIPT_SKELETON = '''

from zipfile import ZipFile
from tarfile import TarFile
import os
import base64
import colorama

if os.name == 'nt': colorama.init()


_PYTHON_INSTALL_TMP_DIR = os.environ['TMP'] if os.name == 'nt' else '/tmp/'
_PYTHON_INSTALL_ARCHIVE_FORMAT = '{format}'

_PYTHON_INSTALL_ARCHIVE_OBJECT = TarFile if _PYTHON_INSTALL_ARCHIVE_FORMAT == 'tar' else ZipFile

_PYTHON_INSTALL_DATA_BIN = #%here goes the data!%
print(colorama.Fore.CYAN, 'building archive...', colorama.Style.RESET_ALL)
with open(os.path.join(
  _PYTHON_INSTALL_TMP_DIR, '~$archive.zip'), 'wb') as f:
    f.write(base64.b64decode(_PYTHON_INSTALL_DATA_BIN.encode()))
print('done')

{lower_code}

'''


class ScriptCompiler:
    """compiles the script and a data directory into one file.
    will extract to {tmp}/~$archive.tmp on runtime.
    """

    def __init__(self, script, data: ArchiveHandler):
        self.script = script
        self.data = data

    def get_data(self,):
        """return text for an installer script"""
        dictionary = {
            'format': self.data.archive_type,
            'lower_code': self.script,
        }
        code = SCRIPT_SKELETON.format(**dictionary)
        upper, lower = code.split('#%here goes the data!%')
        raw = base64.b64encode(
            self.data.get_binary_data())
        with open('.tempfile', 'wb') as openfile:
            openfile.write(upper.encode())
            openfile.write(b"r'''")
            openfile.write(_break(raw))
            openfile.write(b"'''")
            openfile.write(lower.encode())

        code = open('.tempfile', 'rb').read()

        return code

    def dump(self, filename):
        """send the contents of this file to filename"""
        with open(filename, 'wb') as openfile:
            openfile.write(self.get_data())


# def _break(bytes_, num=50):
#     """breaks string at every numth character, and inserts a newline."""
#     pos = 0
#     new = b''
#     for char in bytes_:
#         if pos == num:
#             new += chr(char).encode() + b'\n'
#             pos = 0
#         new += chr(char).encode()
#         pos += 1

#     return new


def _break(bytes_, num=50):
    """breaks string at every numth character, and inserts a newline."""
    new = b''
    old = 0
    for i in range(0, len(bytes_), num):
        new += bytes_[old:i] + b'\n'
        old = i
    new += bytes_[old:]
    return new


if __name__ == '__main__':
    print(_break_test(b'1' * 500).decode())
    # ScriptCompiler(open('archive_data.py').read(),
    #                ArchiveHandler('test-dir')).dump('example.py')
