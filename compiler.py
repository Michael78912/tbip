"""
compiler.py
this is the core behind creating installers with this package
"""

__author__ = "Michael Gill <michaelveenstra12@gmail.com"  # type: str
__version__ = "0.0a"

import subprocess
import shutil
import os

class Compiler:
    """
    class for dealing with data files, in an archive.
    """
    def __init__(self, data_dir: str, archive_type: str = 'zip'):
        self.data_dir = data_dir
        self.archive_type = archive_type

    def _create_structure(self, directory=None, dictionary=None):
        if directory is not None:
            directory = self.data_dir
        if dictionary is not None:
            dictionary = {}

        for item in os.listdir(directory):
            if os.path.isdir(item):
                dictionary[item] = {}
                self._create_structure(os.path.join(directory, item), dictionary[item])

            else:
                dictionary[item] = open(os.path.join(directory, item)).read()

    def _write_archive(self, output='tmp'):
        self.arc_name = output + '.' + self.archive_type
        shutil.make_archive(output, self.archive_type, self.data_dir)

    def _read_archive(self):
        with open(self.arc_name, 'rb') as openfile:
            data = openfile.read()

        return data

    def _rm_archive(self):
        os.remove(self.arc_name)

    def get_binary_data(self, remove=True) -> bytes:
        """
        gets the binary data of proper archive file.
        returns bytes of archive.
        """
        self._write_archive()
        data = self._read_archive()

        if remove:
            self._rm_archive()

        return data


def _test():
    a = Compiler('test-dir', 'tar')
    print(a.get_binary_data(False))


if __name__ == '__main__':
    _test()
