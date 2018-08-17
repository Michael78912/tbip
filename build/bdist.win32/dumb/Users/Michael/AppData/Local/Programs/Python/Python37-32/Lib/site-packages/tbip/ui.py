"""ui.py- base class for all UIs.
inherit ALL UI classes from this, as it wil handle the codes returned
from each item that is run.
"""
import sys


class UI:
    """base class for UIs.
    the method `process` should always be called after every
    item run. all other methods should be overridden.
    """
    codes = {
        0: lambda: None,
        1: sys.exit,
    }

    def __init__(self, items):
        self.items = items

    def process(self, code):
        """proccesses error code and runs proper function."""
        self.codes[code]()

    def run(self):
        """runs all items in proper UI"""
        pass
