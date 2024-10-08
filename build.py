import os, sys

modulePath = '/Users/gferreira/hipertipo/tools/xTools4/Lib'
if modulePath not in sys.path:
    sys.path.append(modulePath)

from importlib import reload
import xTools4
reload(xTools4)
import xTools4.modules.sys
reload(xTools4.modules.sys)

import shutil
import pathlib
from mojo.extensions import ExtensionBundle
from xTools4.modules.sys import pycClear, pyCacheClear, removeGitFiles

# --------
# settings
# --------

version          = xTools4.__version__
baseFolder       = os.path.dirname(__file__)
libFolder        = os.path.join(baseFolder, 'Lib')
licensePath      = os.path.join(baseFolder, 'LICENSE')
extensionPath    = os.path.join(baseFolder, 'xTools4.roboFontExt')
docsFolder       = os.path.join(baseFolder, 'Docs', '_site')

# ---------------
# build extension
# ---------------

def buildExtension():

    B = ExtensionBundle()
    B.name                 = "xTools4"
    B.developer            = 'Gustavo Ferreira'
    B.developerURL         = 'http://hipertipo.com/'
    B.version              = version
    B.launchAtStartUp      = True
    B.html                 = False
    B.mainScript           = 'start.py'
    B.requiresVersionMajor = '4'
    B.requiresVersionMinor = '4'
    B.addToMenu            = [
        {
            'path'          : 'xTools4/dialogs/preferences.py',
            'preferredName' : 'preferences',
            'shortKey'      : '',
        },
    ]
    with open(licensePath) as license:
        B.license = license.read()

    if os.path.exists(extensionPath):
        print('\tdeleting existing .roboFontExt package...')
        shutil.rmtree(extensionPath)

    print('\tbuilding .roboFontExt package...')
    B.save(extensionPath, libFolder=libFolder, htmlFolder=docsFolder)

    errors = B.validationErrors()
    if len(errors):
        print('ERRORS:')
        print(errors)

# ---------------
# build extension
# ---------------

pycClear(baseFolder)
pyCacheClear(baseFolder)
print(f'building xTools4 {version}...\n')
buildExtension()
print('\n...done!\n')

assert os.path.exists(extensionPath)
