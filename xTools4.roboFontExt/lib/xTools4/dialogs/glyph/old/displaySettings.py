from vanilla import *
from mojo.UI import getGlyphViewDisplaySettings, setGlyphViewDisplaySettings, AccordionView
from xTools4.dialogs.old import hDialog


#: A dictionary of section names and checkbox descriptions. Checkboxes are defined by their UI title, and the optional option name (when they differ).
treeTitles = {
    'Glyph' : [
        'Fill',
        'Stroke',
        'Metrics',
        'Anchors',
        'Image',
    ],
    'Points' : [
        ('On Curve',    'On Curve Points'),
        ('Off Curve',   'Off Curve Points'),
        ('Coordinates', 'Point Coordinates'),
        'Labels',
    ],
    'Indexes' : [
        ('Point',       'Point Indexes'),
        ('Segment',     'Segment Indexes'),
        ('Contour',     'Contour Indexes'),
        ('Component',   'Component Indexes'),
        ('Anchor',      'Anchor Indexes'),
    ],
    'Alignment' : [
        'Rulers',
        'Guides',
        'Grid',
        'Blues',
        'Family Blues',
    ],
    'Info' : [
        ('Metrics',     'Metrics Titles'),
        ('Measurement', 'Measurement Info'),
        ('Component',   'Component Info'),
        ('Image',       'Image Info'),
    ],
    'Helpers'   : [
        'Outline Errors',
        'Curve Length',
        'Bitmap',
    ],
}


class GlyphViewDisplayDialog(hDialog):

    '''
    A dialog to toggle display options in the Glyph Editor.

    ::
    
        from hTools3.dialogs.glyph.displaySettings import GlyphViewDisplayDialog
        GlyphViewDisplayDialog()

    '''

    #: A list of sections which are collapsed by default.
    collapsed = [ 'Interface', 'Helpers', 'Info' ]
    
    def __init__(self):

        settings = getGlyphViewDisplaySettings()
        windowHeight = 0
        p = self.padding

        # build interface from treeTitles list
        descriptions = []
        self.checkBoxes = {}
        for sectionTitle, items in treeTitles.items():
            # create panel
            x, y = p, 0
            sectionPanel = Group((0, 0, -0, -0))
            sectionAttr = sectionTitle.lower()
            # populate panel
            for item in items:
                if len(item) == 2:
                    itemTitle, itemSetting = item
                else:
                    itemTitle = itemSetting = item
                itemValue = settings[itemSetting]
                attrTitle = itemTitle.lower().replace(' ', '-')
                attrValue = CheckBox(
                    (x, y, self.width, self.textHeight),
                    itemTitle.lower(),
                    value=itemValue,
                    sizeStyle='small',
                    callback=self.updateViewCallback)
                setattr(sectionPanel, attrTitle, attrValue)
                y += self.textHeight
                self.checkBoxes[itemSetting] = attrValue
            # make description
            sectionHeight = y + p
            description = {
                'label'     : sectionTitle.lower(),
                'view'      : sectionPanel,
                'size'      : sectionHeight,
                'collapsed' : True if sectionTitle in self.collapsed else False,
                'canResize' : False,
            }
            descriptions.append(description)
            # auto calculate window height
            windowHeight += self.textHeight
            if sectionTitle not in self.collapsed:
                windowHeight += sectionHeight
        # create window
        self.w = FloatingWindow(
            (self.width, windowHeight),
            minSize=(self.width, 220),
            maxSize=(self.width, 700),
            title='display')
        # create accordion view
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)
        # open dialog
        self.openWindow()

    @property
    def currentSettings(self):
        '''
        Returns the currently selected display settings as a dictionary.
        
        '''
        settings = {}
        for name, checkbox in self.checkBoxes.items():
            settings[name] = bool(checkbox.get())
        return settings

    def updateViewCallback(self, sender):
        setGlyphViewDisplaySettings(self.currentSettings)


if __name__ == '__main__':
    GlyphViewDisplayDialog()
