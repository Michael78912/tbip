import io
import os

import tbip.installer as install
from tbip.cli import CLI
import tbip.uiutils as utils

LICENCE = """
a fake licence.
"""

README = "Howdy. Bye now, this thing does stuff."


def main():
    installer = install.Installer(
        [], [],
        os.path.join(os.environ.get('HOME')
                     or os.environ.get('USERPROFILE'), 'thing'),
        CLI,
    )

    installer.run()

if __name__ == '__main__':
    main()


