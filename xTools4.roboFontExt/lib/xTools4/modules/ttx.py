import os, sys
import time
from io import StringIO
from xml.etree.ElementTree import parse
from fontTools.ttLib import TTFont


class SuppressPrint(object):

    '''An object to silence console output.'''

    def __init__(self):
        pass

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = StringIO()

    def __exit__(self, *args):
        sys.stdout = self.stdout


def ttx2otf(ttxPath, otfPath=None):
    '''
    Generate an .otf font from a .ttx file.

    Args:
        ttxPath: Path of the .ttx font source.
        otfPath: Path of the target .otf font.

    '''
    # make otf path
    if not otfPath:
        otfPath = ttxPath.replace('.ttx', '.otf')
    # save otf font
    with SuppressPrint():
        tt = TTFont()
        tt.verbose = False
        tt.importXML(ttxPath)
        tt.save(otfPath)
        tt.close()

def otf2ttx(otfPath, ttxPath=None):
    '''
    Generate a .ttx font from an .otf file.

    Args:
        otfPath: Path of the .otf font source.
        ttxPath: Path of the target .ttx font.

    '''
    # make ttx path
    if not ttxPath:
        ttxPath = otfPath.replace('.otf', '.ttx')
    # save ttx font
    with SuppressPrint():
        tt = TTFont(otfPath)
        tt.verbose = False
        tt.saveXML(ttxPath)
        tt.close()

def ttx2ttf(ttxPath, ttfPath=None):
    '''
    Generate a .ttf font from a .ttx file.

    Args:
        ttxPath: Path of the .ttx font source.
        ttfPath: Path of the target .ttf font.

    '''
    # make ttf path
    if not ttfPath:
        ttfPath = ttxPath.replace('.ttx', '.ttf')
    if os.path.exists(ttfPath):
        os.remove(ttfPath)
    # save ttf font
    with SuppressPrint():
        tt = TTFont()
        tt.verbose = False
        tt.importXML(ttxPath)
        tt.save(ttfPath)
        tt.close()

def ttf2ttx(ttfPath, ttxPath=None):
    '''
    Generate a .ttx font from a .ttf file.

    Args:
        ttfPath: Path of the .ttf font source.
        ttxPath: Path of the target .ttx font.

    '''
    # make ttx path
    ttxPath = ttfPath.replace('.ttf', '.ttx')
    if os.path.exists(ttxPath):
        os.remove(ttxPath)
    # save ttx font
    with SuppressPrint():
        tt = TTFont(ttfPath)
        tt.verbose = False
        tt.saveXML(ttxPath)
        tt.close()

def stripNames(ttxPath):
    '''
    Clear several nameIDs to prevent the font from being installable on desktop OSs.

    **ttxPath** Path of the .ttx font to be modified.

    '''
    # nameIDs which will be erased
    nameIDs = [1, 2, 4, 16, 17, 18]
    tree = parse(ttxPath)
    root = tree.getroot()
    for child in root.find('name'):
        if int(child.attrib['nameID']) in nameIDs:
            child.text = ' '
    tree.write(ttxPath)

def setVersionString(ttxPath, text):
    tree = parse(ttxPath)
    root = tree.getroot()
    for child in root.find('name'):
        if child.attrib['nameID'] == '5':
            child.text = text
    tree.write(ttxPath)

def setUniqueName(ttxPath, uniqueName):
    tree = parse(ttxPath)
    root = tree.getroot()
    for child in root.find('name'):
        if child.attrib['nameID'] == '3':
            child.text = uniqueName
    tree.write(ttxPath)

def getUniqueName(ttfPath):
    ID, platformID, platEncID = 3, 3, 1 # mac
    f = TTFont(ttfPath)
    return f['name'].getName(ID, platformID, platEncID)

def setNameIDs(ttxPath, familyName, styleName):
    tree = parse(ttxPath)
    root = tree.getroot()
    for child in root.find('name'):
        # name ID 4: full font name
        if child.attrib['nameID'] == '4':
            child.text = f'{familyName} {styleName}'
        # name ID 6: Postscript name
        if child.attrib['nameID'] == '6':
            child.text = f'{familyName}-{styleName}'
        # name ID 17: preferred subfamily
        if child.attrib['nameID'] == '17':
            child.text = f'{styleName}'
    tree.write(ttxPath)

def setCopyrightTrademark(ttxPath, copyright, trademark):
    tree = parse(ttxPath)
    root = tree.getroot()
    for child in root.find('name'):
        if child.attrib['nameID'] == '0':
            child.text = copyright
        if child.attrib['nameID'] == '7':
            child.text = trademark
    tree.write(ttxPath)

def getVersionString(ttfPath):
    ID, platformID, platEncID = 5, 3, 1 # mac
    f = TTFont(ttfPath)
    return f['name'].getName(ID, platformID, platEncID)

def fixFontInfo(otfPath, familyName, styleName, versionMajor, versionMinor, timestamp=None, trademark=None, copyright=None, ttxClear=True):

    ttxPath       = otfPath.replace('.otf', '.ttx').replace('.ttf', '.ttx')
    if timestamp is None:
        timestamp = time.strftime("%y%m%d%H%M", time.localtime()) # %S seconds
    versionString = f'Version {versionMajor}.{versionMinor}'
    uniqueName    = f'{familyName} {styleName} {timestamp}'

    if not trademark:
        trademark = 'here comes the trademark text'
    if not copyright:
        copyright = 'here comes the copyright text'

    otf2ttx(otfPath, ttxPath)
    setVersionString(ttxPath, versionString)
    setUniqueName(ttxPath, uniqueName)
    setNameIDs(ttxPath, familyName, styleName)
    setCopyrightTrademark(ttxPath, copyright, trademark)
    ttx2otf(ttxPath, otfPath)

    if ttxClear:
        os.remove(ttxPath)

def extractTables(otfPath, destFolder, tableNames=['name'], split=True):
    '''
    Extract font tables from an OpenType font as .ttx.

    '''
    ttfont = TTFont(otfPath)
    info_file = os.path.splitext(os.path.split(otfPath)[1])[0]
    info_path = os.path.join(destFolder, '%s.ttx' % info_file)
    ttfont.saveXML(info_path, tables=tableNames, splitTables=split)
    ttfont.close()

def findAndReplaceOTF(otfPath, destPath, findString, replaceString, tables=['name']):
    ttxPath = '%s.ttx' % os.path.splitext(otfPath)[0]
    otf2ttx(otfPath, ttxPath)
    findAndReplaceTTX(ttxPath, findString, replaceString, tables)
    ttx2otf(ttxPath, destPath)
    os.remove(ttxPath)

def findAndReplaceTTX(ttxPath, findString, replaceString, tables=['name']):
    count = 0

    if 'name' in tables:
        tree  = parse(ttxPath)
        root  = tree.getroot()
        for child in root.find('name'):
            if child.text.find(findString) != -1:
                new_text = child.text.replace(findString, replaceString)
                child.text = new_text
                count += 1
        tree.write(ttxPath)

    if 'CFF ' in tables:
        CFF_elements = ['version', 'Notice', 'Copyright', 'FullName', 'FamilyName', 'Weight']
        ttFont = TTFont()
        ttFont.importXML(ttxPath)
        font_dict = ttFont['CFF '].cff.topDictIndex.items[0]
        for element in CFF_elements:
            text = getattr(font_dict, element)
            if text.find(findString) != -1:
                new_text = text.replace(findString, replaceString)
                setattr(font_dict, element, new_text)
                count += 1
        ttFont.saveXML(ttxPath)
        ttFont.close()

    return count

# ----------
# DSIG table
# ----------

def makeDSIG(ttFont):
    '''
    Create a dummy DSIG table.

    thanks to Ben Kiel on `TypeDrawers`_
    
    .. _TypeDrawers: http://typedrawers.com/discussion/192/making-ot-ttf-layout-features-work-in-ms-word-2010

    '''
    from fontTools import ttLib
    from fontTools.ttLib.tables.D_S_I_G_ import SignatureRecord

    dsig = ttLib.newTable("DSIG")
    dsig.ulVersion = 1
    dsig.usFlag = 1
    dsig.usNumSigs = 1
    sig = SignatureRecord()
    sig.ulLength = 20
    sig.cbSignature = 12
    sig.usReserved2 = 0
    sig.usReserved1 = 0
    sig.pkcs7 = b'\xd3M4\xd3M5\xd3M4\xd3M4'
    sig.ulFormat = 1
    sig.ulOffset = 20
    dsig.signatureRecords = [sig]
    ttFont["DSIG"] = dsig
    # ugly but necessary -> so all tables are added to ttfont
    # ttFont.lazy = False
    # for key in ttFont.keys():
    #     print(ttFont[key])

def addDSIG(otfPath):
    '''
    Add a dummy DSIG table to an OpenType-TTF font.
    This is required to make positioning features work in Office applications on Windows.

    '''
    # with SuppressPrint():
    ttFont = TTFont(otfPath)
    makeDSIG(ttFont)
    ttFont.save(otfPath)
    ttFont.close()

def clearDSIG(otfPath, verbose=True):
    '''Delete DSIG table in the given OpenType font.'''
    ttFont = TTFont(otfPath)
    try:
        del ttFont["DSIG"]
        ttFont.save(otfPath)
    except:
        print("font does not have a 'DSIG' table")
    finally:
        ttFont.close()


