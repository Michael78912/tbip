"""this package is all the cross-UI "Items" for displaying
all of the things needed in an installer, a README, License, etc...
and a tool for actually installing itself.
"""

from enum import Enum
import getpass
import sys
import subprocess
import os

sys.path.append('..')

try:
    from .baseitem import Item
    from .tree import Tree
except SystemError:
    from baseitem import Item
    from tree import Tree


class ProgressUtils(Enum):
    """enumerations of methods of displaying progress."""
    PROGRESS_BAR = 0
    PERCENT = 1
    FILES = 2
    NULL = 3
    MSG = 4


class _CaseInsensitiveDict(dict):

    def __getitem__(self, key):
        return super(_CaseInsensitiveDict, self).__getitem__(key.lower())

    def __setitem__(self, key, val):
        super(_CaseInsensitiveDict, self).__setitem__(key.lower())


class Readme(Item):
    """
    displays a readme.
    """

    def __init__(self, file):
        self.file = file

    def run(self):
        for i in self.file:
            self.ui.echo(i)

        getpass.getpass('press enter to continue...')
        return 0


class Licence(Item):
    """
    displays a licence, and asks if it is OK
    """

    def __init__(self, file):
        self.file = file

    def run(self):
        self.ui.echo('LICENCE:')
        for i in self.file:
            self.ui.echo(i.strip())

        i = ''
        while i not in 'ynYN':
            i = self.ui.get_input('accept? (y/n): ')

        if i in 'yY':
            return 0

        return 1


class Caller(Item):
    """calls an external program"""

    def __init__(self, args):
        self.args = args

    def run(self):
        subprocess.call(self.args)
        return 0


class Choice(Item):
    """asks what they would like to do, and acts accordingly"""

    def __init__(self, msg="continue", opts={'y': lambda: 0, 'n': lambda: 1}, ignorecase=True):
        self.msg = self.form(msg, opts)
        self.opts = _CaseInsensitiveDict(**opts) if ignorecase else opts

    @staticmethod
    def form(msg, opts):
        """forms the message to be sent"""
        return '{} ({}): '.format(msg, '/'.join(opts.keys()))

    def run(self):
        opt = ''
        while opt not in self.opts.keys():
            opt = self.ui.get_input(self.msg)

        return self.opts[opt]


# class Installer(Item):
#     """actually installs the things."""

#     def __init__(self,
#         install_dir,
#         path_to_main=None,:
#         """
#         install_dir is the directory for the thing to be installed.

#         self.dir_tree = map(Tree, data_dirs)
#         self.path_to_main


if __name__ == '__main__':
    Choice().run()
