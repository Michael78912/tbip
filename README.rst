####
TBIP
####

**********************************************
TBIP- Tool for Building Installers with Python
**********************************************
a flexible package to create installers using Python

.. contents::

About
-----

TBIP is a package designed to let you build installers with python,
easily and be very flexible at the same time.

Example
-------
.. code-block:: python

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
            [
                utils.Readme(io.StringIO(README)),
                # a readme class
                utils.Licence(io.StringIO(LICENCE)),
                # a licence class
                utils.Choice('proceed with installation?'),
                # make sure you want to continue
            ],
            [
                utils.Readme(io.StringIO('you installed it. good work.'))
                # output message after installation
            ],
            # install to home directory/thing
            os.path.join(os.environ.get('HOME')
                        or os.environ.get('USERPROFILE'), 'thing'),
            # use the CLI interface
            CLI,
        )

        # run the installer
        installer.run()

    if __name__ == '__main__':
        main()

a very small, but functional example of a script.

Usage
-----
okay, say we had that script saved, and ready to use.
but what is the point? it's not going to actually install 
anything, because you havent even specified where to install!!

that's where the command line comes in handy. you should be able to
run this with :code:`python -m tbip <script-name> -d <data-directory>`.
this will bundle your data in the installer script, as a zip file encoded
in base64, to be extracted at runtime and installed from there on.

Installation
------------
once I get this up on PyPI, you can install
from :code:`pip install tbip`. for now, you can clone it and run it in
the current directory.

Advanced Usage
--------------

Getting Priveleges
^^^^^^^^^^^^^^^^^^

Windows
"""""""

:code:`tbip.get_admin()` should restart the program as an administrator.
if not, the user probably has insufficient rights.

Unix/Linux
""""""""""

:code:`tbip.get_root()` should replace the current program with gksudo, 
nd run it as root.

if it does not work, install gksudo in the package :code:`gksu`, and try again.


Items
^^^^^

*a note on how items interact with their UI*: the UI object
you passed to :code:`Installer` was sent to each of the items you also sent.
when an item's :code:`run` method is called, it is expected to return 1 of 2
values, which is passed to the UI's :

- 0: everything went OK, continue
- 1: something happened, abort

there is a wider variety of  items in tbip.uiutils that can be used during the installation.
they include:

- Readme
- Licence
- Caller
- Choice

Readme
""""""
displays a readme, and tells the user to press enter to continue.

:code:`Readme(file)` --> tbip.uiutils.Readme object

Licence
"""""""
displays a licence, preceded by the header "LICENCE:".
aks the user if this is OK and wants to continue.

:code:`Licence(file)` --> tbip.uiutils.Licence object

Caller
""""""
calls an external program, with the arguments specified.
just a very thin wrapper around :code:`subprocess.call`.

:code:`Caller(args)` --> tbip.uiutils.Caller object

Choice
""""""
prompts the user for a string, and acts accordingly.
if the string enterd is not valid, prompt again.

:code:`Choice(msg="continue?", opts={'y': lambda: 0, 'n': lambda: 1}, ignorecase=True)` --> tbip.uiutils.Choice object

Installation progress
^^^^^^^^^^^^^^^^^^^^^

there are sevreal ways to watch the installation progress
(all accessed in :code:`tbip.installer.ProgressUtils`)

+--------------------------------+------------------------------------+-----------+
|          Description           |            name                    |  value    |
+================================+====================================+===========+
|          a progress bar        | :code:`ProgressUtils.PROGRESS_BAR` |    0      |
+--------------------------------+------------------------------------+-----------+
|           percentage           |   :code:`ProgressUtils.PERCENT`    |    1      |
+--------------------------------+------------------------------------+-----------+
| displaying each file processed |   :code:`ProgressUtils.FILES`-     |    2      |
+--------------------------------+------------------------------------+-----------+
|     do absolutely nothing      |     :code:`ProgressUtils.NULL`     |    3      |
+--------------------------------+------------------------------------+-----------+
|  at first, display a message   |      :code:`ProgressUtils.MSG`     |    4      |
+--------------------------------+------------------------------------+-----------+

Command Line options
^^^^^^^^^^^^^^^^^^^^

tbip uses PyInstaller_ internally to freeze the output scripts.

.. _PyInstaller: https://www.pyinstaller.org/

Miscellaneous:

-h, --help              display help
-v, --version           display version information

-d, --data <dir>        bundle this data with script in a zip file
-o <output>             output filename of script
-f, --freeze            freeze the installer script

PyInstaller specific:

-u, --upx <dir>         directory where UPX_ is installed (if at all)
-w, --windowed          use no console window (Windows specific)
-i, --icon <icon>       path to icon file (Windows specific)

.. _UPX: https://upx.github.io/

Deriving classes
^^^^^^^^^^^^^^^^

only the classes UI and Item should be derived from. find the base classes for:

- UI: :code:`tbip.ui.UI`
- Item: :code:`tbip.uiutils.baseitem.Item`

User Interfaces
"""""""""""""""

the CLI (Command Line Interface) is a UI. you can see here:

.. code-block::python

    class _CLI(UI):
    """class for handling all of the sending of items, and runs them in order."""

    ProgressBar = ProgressBar

    class Percent:
        ...

        def __init__(self, outfile=sys.stdout, infile=sys.stdin):
            ...

        def echo(self, *args, fcolour=colorama.Fore.WHITE,
            ...

        def get_input(self, prompt='', length='*', strip=True):
        ...

        @staticmethod
        def getch(echo=True):
            ...

        @staticmethod
        def clear():
            ...

all those methods should be overridden in a new class.
(I actually haven't used :code:`getch` yet, but i might, so it would be good to)

they all should be self explanitory, but:

:code:`echo` outputs the message to the screen in CLI it is just a wrapper around `print`. 
it should be able to take all of the arguments you see there, and act accordingly.

:code:`get_input` should be able to read one line. the length parameter acts a bit like quantifiers in a regex.
?: truncate it to one character, or 0
+: will return if the string is one character or more, if it is null, will prompt again.
*: any length (including 0)

(of course, any integer will work too)

:code:`getch` should read a single character. if echo is true, echo the character too.

:code:`clear` should simply clear the display

Items
"""""

Items are easier. here is :code:`Caller`:

.. code-block::python

    class Caller(Item):
    """calls an external program"""

    def __init__(self, args):
        self.args = args

    def run(self):
        subprocess.call(self.args)
        return 0

simple, short and sweet. of course, this is a minimal example,
you can create any item you want to do anything you want!

it must have :code:`run` overridden, because if you didn't, it would do nothing.
*remember that :code:`run` must always return 1 or 0!*

Contributing
------------

any help is appreciated. if you want to help, please fork_ this repository,
and create a pull request when you want to. also, please note any bugs,
and if you have any suggestions, I would be glad to try them! thank you!

.. _fork: https://github.com/Michael78912/tbip/fork

In the Future
-------------

I plan on making a GUI User interface. this is probably top of my list on things to
do. once again, if you have any suggestions, either make an issue, or email me at
michael.78912.8@gmail.com






