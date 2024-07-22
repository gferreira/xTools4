import os, sys

print('initializing hTools4...\n')

# add module
libFolder = os.getcwd()
print('\tadding hTools4 module to sys.path...')
sys.path.append(libFolder)

# add menu
from hTools3.modules.sys import add_hTools4_menu_main
add_hTools4_menu_main('menus', verbose=True)

print('\n...done.\n')
