"""
this file will create the installer itself.
"""


try:
    from .compiler import ScriptCompiler

except ImportError:
    # debug mode
    from compiler imoport ScriptCompiler



class Installer:
    def __init__(
        self,
        script,
        items, 
        data=None,
        ui=ui.Cli,

        )