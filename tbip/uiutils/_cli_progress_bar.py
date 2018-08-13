"""
console.py- this deals with console programs and things like that
"""

import shutil


class ProgressBar:
    finished = False

    def __init__(self, increments_to_full, title=''):
        self.title = title
        self.increments_to_full = increments_to_full
        self.increments_completed = 0

    def calc_percent(self, increments_completed) -> float:
        """

        :param increments_completed: the amount of increments the progress bar has completed
        :return: the percentage complete of the progress bar
        """
        perc = (increments_completed / 100) * self.increments_to_full
        if round(perc) >= 100:
            self.finished = True
        return perc

    def write(self, title='', nonewline=True, flush=True, filler='#', not_done=' ') -> None:
        """
        writes proper progress bar string to sys.stdout
        :param title: title displayed at beginning of bar
        :param nonewline: set to False if you want the
        :param flush: flush sys.stdout if set to True
        :param filler: the filling of done progress
        :param not_done: the filler of not completed progress
        :return: None
        """
        # initialize string
        string = self.genstr(title, filler, not_done)
        if nonewline:
            # add carriage return code
            string = '\r' + string
        # send to sys.stdout
        print(string, end='\b', flush=flush)

    def genstr(self, title, filler='#', not_done=' ') -> str:
        """
        generates the string of the current progress bar
        :return: that string
        """

        # initialize string
        string = title + ' |'
        # determine amount to put filler
        filler_amount = round(self.calc_percent(
            self.increments_completed)) // 2
        # determine amount to fill with not done progress
        not_done_amount = 50 - filler_amount
        # add items to progress bar
        string += (filler * filler_amount) + (not_done * not_done_amount) + '|'
        # add percentage to end of string
        string += ' ' + \
            repr(round(self.calc_percent(self.increments_completed))) + '%'
        # pad with whitespace, as to knock over previous stuff
        string = string.ljust(shutil.get_terminal_size()[0] - 1, ' ')
        return string

    def increment(self, amount) -> None:
        """
        adds amount to self.increments_completed
        :param amount: amount to add
        :return: None
        """
        self.increments_completed += amount

    def add(self, amount, filler='\u2588', not_done=' ') -> None:
        """
        calls increment, and write in turn
        :param amount: amount completed
        :param filler: what to fill finished amount with
        :param not_done: the character to fill unfinished space with
        :return: None
        """

        self.increment(amount)
        self.write(self.title, filler=filler, not_done=not_done)


def _test():
    import time
    s = ConsoleProgressBar(100, 'test')
    while not s.finished:
        s.add(0.5)
        time.sleep(0.01)


if __name__ == '__main__':
    _test()
