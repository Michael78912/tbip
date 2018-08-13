"""baseitem.py- base class for ui items in tbip
these "items" should be compatible with *all* UI classes.
that's why a UI object will be passed to "set"
"""


class Item:

    def run(self):
        """to be overridden.
        run when used in a sequence of the 
        commands, when sent to installer.
        """
        pass

    def set(self, ui):
        """set the UI to self."""
        self.ui = ui

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)
