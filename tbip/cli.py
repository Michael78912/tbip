"""CLI: command line interface installer.
you will create a CLI object, and pass it to installer.
"""

import sys
import colorama

_MS_WINDOWS = sys.platform == 'win32'

try:
    from .uiutils._cli_progress_bar import ProgressBar
    from .ui import UI

except SystemError:
    from uiutils._cli_progress_bar import ProgressBar
    from ui import UI


if _MS_WINDOWS:
    import msvcrt
    _getche = msvcrt.getwche
    _getch = msvcrt.getwch

else:
    import tty
    import termios

    def _getch():
        file_descriptor = sys.stdin.fileno()
        old = termios.tcgetattr(file_descriptor)
        try:
            tty.setraw(file_descriptor)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old)
        return char

    def _getche():
        char = _getch()
        sys.stdout.write(char)
        sys.stdout.flush()
        return char


def _contains(string, sub):
    if isinstance(sub, str):
        return sub in string
    return False


class _CLI(UI):
    """class for handling all of the sending of items, and runs them in order."""

    ProgressBar = ProgressBar

    class Percent:
        """class for displaying percent completed of installation"""
        finished = False
        increments_completed = 0

        def __init__(self, increments_to_full, title='progress: '):
            self.increments_to_full = increments_to_full
            self.title = title

        def add(self, amount):
            """adds an amount to self.increments_completed,
            and displays the updated thing.
            """
            self.increments_completed += amount
            perc = (self.increments_completed / 100) * self.increments_to_full
            if round(perc) >= 100:
                self.finished = True

            print('\r{}%'.format(perc))

    def __init__(self, outfile=sys.stdout, infile=sys.stdin):
        self.outfile = outfile
        self.infile = infile

    def echo(self, *args, fcolour=colorama.Fore.WHITE,
             bcolour=colorama.Back.BLACK, flush=True, newline=True):
        """send output to proper file"""

        print(fcolour, bcolour, ' '.join(args), colorama.Style.RESET_ALL,
              flush=flush, file=self.outfile, end='\n' if newline else '')

    def get_input(self, prompt='', length='*', strip=True):
        """gets input, and and truncates it to length.
        the regexp symbols ?, +, and * can also be used.
        ?: truncate it to one character, or 0
        +: will return if the string is one character or more, if it is null, will prompt again.
        *: any length (including 0)
        any number will also work, and will prompt again if less, and truncate if more
        """

        # make sure the symbol/number is proper
        if not _contains('+*?', length) and not isinstance(length, int) and length > 0:
            raise ValueError(
                'length must be integer greater than 0 or a ?, +, or * symbol.')

        # different function is needed for a number value. prompt again if it
        # is
        if isinstance(length, int):
            func = lambda x: x[:length] if len(x) >= length else None

        else:
            func = {
                '?': lambda x: x[0] if x else '',
                '+': lambda x: x if x else None,
                '*': lambda x: x,
            }[length]

        data = ''
        invalid = False

        while not invalid:
            self.echo(prompt, newline=False)
            data = func(self.infile.readline())
            invalid = False
            if data is not None:
                invalid = True

        return data.strip() if strip else data

    @staticmethod
    def getch(echo=True):
        """get a single character from STDIN without waiting for the return
        key to be pressed.
        if echo is True then display the character.
        """

        return _getche() if echo else _getch()

    @staticmethod
    def clear():
        """works in a similar way to clear on *NIX systems
        and cls on windows.
        """

        # colorama module must be initiated on windows for this to work
        if _MS_WINDOWS:
            colorama.init()

        # ansii escape code for clear
        print("\033[H\033[J")

CLI = _CLI()


if __name__ == '__main__':
    print(CLI().get_input(': ', length=9))
