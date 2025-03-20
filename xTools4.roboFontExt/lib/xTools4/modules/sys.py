import os
import subprocess
import shutil
import sys
from AppKit import NSApp, NSMenu, NSMenuItem
try:
    from mojo.UI import setScriptingMenuNamingShortKeyForPath, createModifier
    from lib.UI.fileBrowser import RFPathItem
except:
    pass

def addMenu(name, path):
    '''
    Creates a new menu in RoboFont's main application menu.

    ::

        menuFolder = 'path/to/menuFolder'
        addMenu('myMenu', menuFolder)

    '''
    # create a new menu
    menu = NSMenu.alloc().initWithTitle_(name)

    # create a path item that will build the menu and connect all the callbacks
    pathItem = RFPathItem(path, ['.py'], isRoot=True)
    pathItem.getMenu(title=name, parentMenu=menu)

    # get the main menu
    menubar = NSApp().mainMenu()

    # search if the menu item already exists
    newItem = menubar.itemWithTitle_(name)
    if not newItem:
        # if not, create one and append it before `Help`
        newItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(name, '', '')
        menubar.insertItem_atIndex_(newItem, menubar.numberOfItems()-1)

    # set the menu as submenu
    newItem.setSubmenu_(menu)

def pycClear(folder, verbose=True):
    '''
    Recursively remove all .pyc files inside a folder.

    ::

        folder = 'path/to/folder'
        pycClear(folder)

    '''
    for fileName in os.listdir(folder):
        filePath = os.path.join(folder, fileName)
        if os.path.splitext(fileName)[-1] == '.pyc':
            if verbose:
                print('deleting %s...' % filePath)
            os.remove(filePath)
        elif os.path.isdir(filePath):
            pycClear(filePath)

def pyCacheClear(folder, verbose=True):
    '''
    Recursively remove all __pycache__ folders inside a folder.

    ::

        folder = 'path/to/folder'
        pyCacheClear(folder)

    '''
    for fileName in os.listdir(folder):
        filePath = os.path.join(folder, fileName)
        if fileName == '__pycache__':
            shutil.rmtree(filePath)
        elif os.path.isdir(filePath):
            pyCacheClear(filePath)

def openPDF(pdfPath):
    '''
    Open a PDF file in macOS Preview app.

    ::

        pdfPath = '/path/to/folder/test.pdf'
        openPDF(pdfPath)

    '''
    subprocess.call(['open', '-a', 'Preview', pdfPath])

def removeGitFiles(extensionPath, verbose=False):

    libFolder = os.path.join(extensionPath, 'Lib')
    folder, extensionFile = os.path.split(extensionPath)

    if verbose:
        print('removing git files from %s...\n' % extensionFile)

    if not os.path.exists(libFolder):
        print("\t('Lib' folder does not exist) %s" % libFolder)
        return

    # remove .git repository
    gitPath = os.path.join(libFolder, '.git')
    if not os.path.exists(gitPath):
        if verbose:
            print('\t(.git file does not exist) %s' % gitPath)
        return

    if verbose:
        print('\tremoving .git data... %s' % gitPath)
    shutil.rmtree(gitPath)

    # remove gitignore file
    gitignorePath = os.path.join(libFolder, '.gitignore')
    if os.path.exists(gitignorePath):
        if verbose:
            print('\tremoving .gitignore file... %s' % gitignorePath)
        os.remove(gitignorePath)

    if verbose:
        print('\n...done.\n')

def buildDocsHTML(sourceFolder, buildFolder, incremental=True, verbose=True):

    htmlFolder     = os.path.join(buildFolder, 'html')
    doctreesFolder = os.path.join(buildFolder, 'doctrees')

    # see `sphinx-build -h` for docs on sphinx options
    commands = ['/usr/local/bin/sphinx-build']

    # build all files (not just new and changed)
    if not incremental:
        commands += ['-a']

    # builder: html / pdf / epub / text / etc.
    commands += ['-b', 'html']

    # supress console warnings and errors
    if not verbose:
        commands += ['-Q']

    # define source and output folders
    commands += ['-d', doctreesFolder]
    commands += [sourceFolder, htmlFolder]

    # delete build folder
    if os.path.exists(buildFolder):
        shutil.rmtree(buildFolder)

    # run sphinx command
    p = subprocess.Popen(commands)
    stdout, stderr = p.communicate()

    if verbose:
        if stdout: print(stdout)
        if stderr: print(stderr)

def timer(start, end):
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"total elapsed time: {int(hours):0>2} hours {int(minutes):0>2} minutes {seconds:05.2f} seconds")

# ---------------
# xTools4 startup
# ---------------

def add_xTools4_menu_main(folderName, verbose=False):
    folderName = os.path.join(os.getcwd(), folderName)
    if verbose:
        print('\tadding xTools4 to the main application menu...')
    addMenu('xTools4', folderName)

def add_xTools4_menu_contextual_font(folderName, verbose=False):
    if verbose:
        print('\tadding xTools4 to the Font Overview contextual menu...')
    pass

