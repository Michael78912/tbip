"""
this file will create the installer itself.
"""

from enum import Enum
import shutil
import os
import sys
import zipfile

_MS_WINDOWS = sys.platform == 'win32'
TMP = os.environ['TMP'] if _MS_WINDOWS else '/tmp'

# error message to be shown if the archive does not exist in
# {tmp}/~$archive.tmp. this means that it has not been extracted from the
# script, as it would if the script was a proper tbip file, run through
# the compiler.
ERR_MSG = """the file {} does not exist.
this means that whoever wrote this script, (hopefully you) has not run your installer
script through the compiler yet, which bundles the data with the script. run
`tbip <installer script name> -d <data directory>` to bundle these together. if you are
not the developer, then contact the actual developer and tell them to fix it, or try
and fix it yourself :)""".format(os.path.join(TMP, '~$archive.zip'))


class ProgressUtils(Enum):
    """enumerations of methods of displaying progress."""
    PROGRESS_BAR = 0
    PERCENT = 1
    FILES = 2
    NULL = 3
    MSG = 4


class Installer:
    """script to create the installer itself."""

    def __init__(
            self,
            pre_install_items,
            post_install_items,
            install_dir,
            ui,
            install_progress=ProgressUtils.PROGRESS_BAR,
    ):
        """items is a sequence of all items that will
        be run in the installation process. ui is the user interface that
        all the items will be run in. application_name is the name of the application.
        install_progress is an enumeration value,
        in ProgressUtils. they are self-explanitory."""

        self.install_dir = install_dir
        self.post_install_items = post_install_items
        self.pre_install_items = pre_install_items
        self.ui = ui
        self.install_progress = install_progress
        for item in post_install_items + pre_install_items:
            item.set(ui)

    def run(self):
        """run all the items given in the proper UI, and
        install.
        """

        for item in self.pre_install_items:
            self.ui.process(item.run())

        self._extract()

        for item in self.post_install_items:
            self.ui.process(item.run())

    def _extract(self):
        """extract the items"""
        try:
            print(os.path.join(TMP, '~$archive.zip'))
            zipf = zipfile.ZipFile(os.path.join(TMP, '~$archive.zip'))

        except FileNotFoundError:
            print(ERR_MSG, file=sys.stderr)
            sys.exit(1)
        dest = self.install_dir
        meter = self.install_progress

        sendf = False

        if meter == ProgressUtils.PROGRESS_BAR:
            meter = self.ui.ProgressBar

        elif meter == ProgressUtils.PERCENT:
            meter = self.ui.Percent

        elif meter == ProgressUtils.FILES:
            sendf = True
            meter = lambda x: print('extracted', x)

        elif meter == ProgressUtils.MSG:
            print('extracting files...')
            meter = lambda _: None
            sendf = True

        elif meter == ProgressUtils.NULL:
            sendf = True
            meter = lambda _: None

        else:
            raise ValueError('invalid progress shower')

        # check that the directory exists
        if os.path.isdir(dest):
            shutil.rmtree(dest)

        # if the file exists, and is a file, remove it!
        if os.path.exists(dest):
            os.remove(dest)

        contents = zipf.infolist()

        # initialize meter with the amount of
        if not sendf:
            meter = meter(len(contents))

        for i, item in enumerate(contents):
            zipf.extract(item, dest)
            if sendf:
                meter(item.filename)
            else:
                meter.add(i)

        self.ui.clear()
