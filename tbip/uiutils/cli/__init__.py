
import getpass
import sys
import subprocess
sys.path.append('..')

from baseitem import Item


class _CaseInsensitiveDict(dict):

    def __getitem__(self, key):
        return super(_CaseInsensitiveDict, self).__getitem__(key.lower())

    def __setitem__(self, key, val):
        super(_CaseInsensitiveDict, self).__setitem__(key.lower())


class Readme(Item):
    """
    displays a readme.
    """

    def __init__(self, ui, file):
        self.ui = ui
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

    def __init__(self, ui,  file):
        self.file = file
        self.ui = ui

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

    def __init__(self, ui, args):
        self.args = args

    def run(self):
        subproces.call(self.args)
        return 0


class Choice(Item):
    """asks what they would like to do, and acts accordingly"""

    def __init__(self, ui, msg="continue", opts={'y': lambda: 0, 'n': lambda: 1}, ignorecase=True):
        self.msg = self.form(msg, opts)
        self.opts = _CaseInsensitiveDict(**opts) if ignorecase else opts

    @staticmethod
    def form(msg, opts):
        return '{} ({}): '.format(msg, '/'.join(opts.keys()))

    def run(self):
        opt = ''
        while opt not in self.opts.keys():
            opt = self.ui.get_input(self.msg)

        return self.opts[opt]


if __name__ == '__main__':
    Choice().run()
