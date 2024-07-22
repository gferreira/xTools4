# menuTitle : preferences

from importlib import reload
import hTools4.dialogs.preferences
reload(hTools4.dialogs.preferences)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.preferences import PreferencesDialog

OpenWindow(PreferencesDialog)