"""
baseitem.py- base class for ui items in python-install
"""


class Item:

    def run(self):
        """
        to be overridden.
        run when used in a sequence of the 
        commands, when sent to installer.
        """
        pass

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)
