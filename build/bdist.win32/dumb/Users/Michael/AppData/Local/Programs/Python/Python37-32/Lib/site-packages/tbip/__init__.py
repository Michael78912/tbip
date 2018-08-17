"""
python_installer- a package for creating installers with python.

project started: June 3, 2018
"""

__author__ = "Michael Gill <michaelveenstra12@gmail.com>"
__version__ = '0.0a'

import sys
import ctypes
import subprocess
import os
import colorama

_MS_WINDOWS = sys.platform == 'win32'

if _MS_WINDOWS:
    colorama.init()


# ============================================================================
# |  the following functions are designed to be helper functions *only*.     |
# |                they are often platform-specific too.                     |
# ============================================================================


def get_admin():
    """check if the user is an Adminstrator (on windows)
    rerun the program, asking for permissions if not.
    """
    if _MS_WINDOWS:
        raise NotImplementedError(
            'Not implemented on %s systems!' % sys.platform)

    if not ctypes.windll.shell32.IsUserAnAdmin():
        # create empty string for arguments
        args = ""
        for arg in sys.argv:
            args += '"{}" '.format(arg)

        # request elevation and run again
        ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, args, None, 1)


def get_root():
    """request root access.
    if gksudo is not installed, will return 1.
    """
    if sys.platform == 'win32':
        # if this code ever gets executed, you need some help
        raise NotImplementedError('there is no root user on Windows')

    if os.geteuid() == 0:
        # is root
        return 0

    code = subprocess.call(['type', 'gksudo'], stdout=open(
        '/dev/null'), stderr=open('/dev/null'))
    if code == 1:
        # command not found
        return 1

    os.execv('/usr/bin/gksudo', ['gksudo'] + sys.argv)
    return 0
