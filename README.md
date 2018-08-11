# TBIP
## Tool for Building Installers with Python


this module aims at being a very flexible package, used to build an installer, with very many options.  
it is able to have multiple data files, built into a single script, using an archive, which is then put in the installer script as a string.
it should support multiple interfaces, including a CLI, a GUI, and one with no interaction at all. you should also be able to design your own,
with a bit more work.  
it will use [pyinstaller](https://github.com/pyinstaller/pyinstaller) internally to make freeze the installer script, and cross-platform  