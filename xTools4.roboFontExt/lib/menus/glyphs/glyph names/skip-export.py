# menuTitle : skip export

from importlib import reload
import xTools4.modules.fontutils
reload(xTools4.modules.fontutils)

from xTools4.modules.fontutils import getGlyphs2
from xTools4.modules.messages import noFontOpen, noGlyphSelected, showMessage

# TODO: read global settings
messageMode = 1
verbose = True

def skipExportGlyphs(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    selectedGlyphs = getGlyphs2(font, glyphNames=False, template=False)

    if not len(selectedGlyphs):
        if verbose:
            showMessage(noGlyphSelected, messageMode)
        return

    skipExportGlyphs = font.lib.get('public.skipExportGlyphs', [])

    for glyph in selectedGlyphs:
        if glyph.name in skipExportGlyphs:
            skipExportGlyphs.remove(glyph.name)
        else:
            skipExportGlyphs.append(glyph.name)
        
    if verbose:
        print("toggle 'skip export' flag...\n")

    font.lib['public.skipExportGlyphs'] = skipExportGlyphs

    for glyph in selectedGlyphs:
        if verbose:
            print(f"\t{glyph.name} [{['export', 'skip'][int(glyph.name in skipExportGlyphs)]}]...")
        glyph.changed()

    font.changed()

    print('\n...done.\n')


if __name__ == '__main__':

    skipExportGlyphs(CurrentFont())
