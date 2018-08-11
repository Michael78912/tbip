"""
this file will create the installer itself.
"""


try:
    from .cli import CLI
    from .compiler import ScriptCompiler

except ImportError:
    # debug mode
    from compiler imoport ScriptCompiler
    from cli import CLI


_CLI = CLI()

class Installer:

    def __init__(
        self,
        script,
        items,
        data=None,
        ui=_CLI,

    )
