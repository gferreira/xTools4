from defcon import Font
from fontTools.designspaceLib import DesignSpaceDocument
from fontMath.mathGlyph import MathGlyph
from mutatorMath.objects.mutator import Mutator, buildMutator


class GlyphCalculator:
    
    def __init__(self, font, designspacePath):
        self.font = font
        self.designspace = DesignSpaceDocument()
        self.designspace.read(designspacePath)
        # pre-load source fonts
        for src in self.designspace.sources:
            src.font = Font(src.path)

    @property
    def default(self):
        return self.designspace.findDefault().location

    def calculate(self, glyphName, location, roundGeometry=True):

        g = self.font[glyphName].naked()

        # patch parameters dict with default values
        default = self.designspace.findDefault().location
        for k, v in default.items():
            if k not in location:
                location[k] = v

        # get designspace axes
        axes = {}
        for axis in self.designspace.axes:
            axes[axis.name] = {}
            for k in ['tag', 'name', 'minimum', 'default', 'maximum', 'map']:
                axes[axis.name][k] = getattr(axis, k)

        # get masters for glyph
        glyphMasters = []
        for src in self.designspace.sources:
            if glyphName in src.mutedGlyphNames:
                continue
            d = dict(font=src.font, location=src.location, glyphName=glyphName)
            glyphMasters.append(d)

        # get location for each master
        items = []
        for item in glyphMasters:
            locationObject = item['location']
            fontObject     = item['font']
            glyphName      = item['glyphName']
            if not glyphName in fontObject:
                continue
            glyphObject = MathGlyph(fontObject[glyphName])
            items.append((locationObject, glyphObject))

        # build mutator and calculate glyph
        bias, m = buildMutator(items, axes=axes)
        instanceObject = m.makeInstance(location)

        if roundGeometry:
            instanceObject = instanceObject.round()

        targetGlyphObject = self.font[glyphName].naked()
        targetGlyphObject.clear()

        instanceObject.extractGlyph(targetGlyphObject, onlyGeometry=True)

