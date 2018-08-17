"""main module for compiling scripts together, with all their data."""

import argparse
import sys
import os
import subprocess

from .archive_data import ArchiveHandler
from . import compiler


def main():
    """parse arguments and act accordingly"""

    parser = argparse.ArgumentParser(
        description="bundle installer scripts and their data",
        prog='tbip')
    parser.add_argument('script', help='script to compile with data')
    parser.add_argument('-d', '--data', dest='data',
                        help='data directory to bundle with script')
    parser.add_argument('-o', dest='output',
                        help='output filename', default='install.py')
    parser.add_argument(
        '-f', '--freeze',
        help='freeze the output script with pyinstaller',
        action='store_true')
    parser.add_argument('-u', '--upx-dir',
                        help='directory to upx.', dest='upx')

    parser.add_argument(
        '-w', '--windowed',
        help='windows specific: make no console window display.',
        action='store_true')

    parser.add_argument(
        '-i', '--icon', help='windows specific: use this icon in the executable')

    parser.add_argument('-v', '--version',
                        action='version', version='0.0 alpha')

    ns = parser.parse_args()

    print('creating, reading and formatting zip file, please wait...'
          '(this may take a while)')
    with open('example.so', 'w') as d:
        d.write(repr(ns))
    make(ns.script, ns.data, ns.output)

    if ns.freeze:
        commands = [
            os.path.join(os.path.dirname(sys.executable),
                         'Scripts', 'pyinstaller')
            if sys.platform == 'win32' else 'pyinstaller',
            ns.output,
            '--onefile',
            '--upx-dir=' + ns.upx if ns.upx is not None else '/',
        ]

        if sys.platform == 'win32':
            commands.append('-w' if ns.windowed else '-c')

        if sys.platform == 'win32' and ns.icon:
            commands.append('-i=' + ns.icon)

        print('running pyinstaller on %s with args %s' %
              (ns.script, ' '.join(commands)))
        subprocess.call(commands)


def make(file, data, dest):
    """combines data with file and puts it in dest."""
    try:
        openfile = open(file)

    except FileNotFoundError:
        print('%s is not found' % file, file=sys.stderr)
        sys.exit(1)

    except PermissionError:
        if os.path.isdir(file):
            print('%s is a directory!' % file, file=sys.stderr)
            sys.exit(1)

        print('Permission denied to %s' % file, file=sys.stderr)
        sys.exit(1)

    compiler.ScriptCompiler(openfile.read(), ArchiveHandler(data)).dump(dest)

main()
