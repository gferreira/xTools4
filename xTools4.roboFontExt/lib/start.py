import os, sys

print('initializing xTools4...\n')

# add xTools4 module to sys.path
libFolder = os.getcwd()
print('\tadding xTools4 module to sys.path...')
sys.path.append(libFolder)

# add xTools4 entry in main menu
from xTools4.modules.sys import add_xTools4_menu_main
add_xTools4_menu_main('menus', verbose=True)

print('\n...done.\n')
