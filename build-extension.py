import os, sys

modulePath = '/Users/gferreira/hipertipo/tools/hTools3/Lib'
if modulePath not in sys.path:
    sys.path.append(modulePath)

from importlib import reload
import hTools3
reload(hTools3)
import hTools3.modules.sys
reload(hTools3.modules.sys)

import shutil
import pathlib
from mojo.extensions import ExtensionBundle
from hTools3.modules.sys import pycClear, pyCacheClear, removeGitFiles

# --------
# settings
# --------

version          = hTools3.__version__
baseFolder       = os.path.dirname(__file__)
libFolder        = os.path.join(baseFolder, 'Lib')
licensePath      = os.path.join(baseFolder, 'license.txt')
resourcesFolder  = os.path.join(baseFolder, 'Resources')
imagePath        = os.path.join(resourcesFolder, 'punch.png')

folderName       = os.path.basename(baseFolder)
folderParent     = os.path.dirname(baseFolder)
extensionsFolder = os.path.join(folderParent, '_extensions')
outputFolder     = os.path.join(extensionsFolder, folderName)
extensionPath    = os.path.join(outputFolder, 'hTools3.roboFontExt')
docsFolder       = None # os.path.join(outputFolder, 'docs', '_site')

# ---------------
# build extension
# ---------------

def buildExtension():

    pycOnly = False # [ "3.6", "3.7" ]

    B = ExtensionBundle()
    B.name                 = "hTools3"
    B.developer            = 'Gustavo Ferreira'
    B.developerURL         = 'http://hipertipo.com/'
    B.icon                 = imagePath
    B.version              = version
    B.expireDate           = '' # '2020-12-31'
    B.launchAtStartUp      = True
    B.html                 = False
    B.mainScript           = 'start.py'
    # B.uninstallScript      = ''
    B.requiresVersionMajor = '3'
    B.requiresVersionMinor = '4'
    B.addToMenu = [
        {
            'path'          : 'docs-user.py',
            'preferredName' : 'docs user',
            'shortKey'      : '',
        },
        {
            'path'          : 'docs-dev.py',
            'preferredName' : 'docs API',
            'shortKey'      : '',
        },
    ]
    with open(licensePath) as license:
        B.license = license.read()

    if os.path.exists(extensionPath):
        print('\tdeleting existing .roboFontExt package...')
        shutil.rmtree(extensionPath)

    menusFolder = os.path.join(libFolder, 'menus')
    pycExcludeFiles = []
    for root, dirs, files in os.walk(menusFolder):
        for fileName in files:
            filePath  = pathlib.Path(fileName)
            if filePath.suffix == '.py':
                filePath = pathlib.Path(root) / fileName
                filePath = list(filePath.parts[5:])
                filePath = os.path.join(*filePath)
                pycExcludeFiles.append(filePath)

    print('\tbuilding .roboFontExt package...')
    B.save(extensionPath,
        libFolder=libFolder,
        # htmlPath=None, # docsFolder,
        resourcesFolder=resourcesFolder,
        # pycExclude=pycExcludeFiles,
        # pycOnly=pycOnly
    )

    errors = B.validationErrors()
    if len(errors):
        print('ERRORS:')
        print(errors)

# ---------------
# build extension
# ---------------

pycClear(baseFolder)
pyCacheClear(baseFolder)
print(f'building hTools3 {version}...\n')
buildExtension()
print('\n...done!\n')
