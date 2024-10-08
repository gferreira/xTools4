'''
A very simple ``mark`` feature builder for accented glyphs.

'''

class markToBaseFeaBuilder:

    '''
    An object to create mark feature code from a list of base glyphs and mark glyphs with named anchors.

    ::

        from hTools3.modules.markFeature import markToBaseFeaBuilder

        f = CurrentFont()

        markToBaseDict = {
            'x'     : [('tildecmb', 'top'), ('gravecmb', 'top'), ('cedillacmb', 'bottom')],
            'X'     : [('tildecmb', 'top')],
            'one'   : [('tildecmb', 'top'), ('cedillacmb', 'bottom')],
            'two'   : [('gravecmb', 'top')],
            'three' : [('tildecmb', 'top')],
        }

        M = markToBaseFeaBuilder(f, markToBaseDict)
        M.verbose = True
        M.buildDicts()
        M.write()

        print(f.features.text)

    '''

    verbose = True

    def __init__(self, font, markToBaseDict):
        self.font = font
        self.markToBaseDict = markToBaseDict
        self.marksDict = {}
        self.basesDict = {}

    @property
    def allBases(self):
        '''Returns a list of all base glyph names.'''
        return self.basesDict.keys()

    @property
    def allMarks(self):
        '''Returns a list of all mark glyph names.'''
        return self.marksDict.keys()

    @property
    def allMarkClasses(self):
        '''Returns a list of all mark class names.'''
        return [self.makeMarkClassName(m) for m in self.allMarks]

    @property
    def fontName(self):
        '''Returns the name of the font.'''
        return '%s %s' % (self.font.info.familyName, self.font.info.styleName)

    def makeMarkClassName(self, markName):
        '''Creates a mark class name for the given mark name.'''
        return '@%s_marks' % markName

    def writeMarkClasses(self):
        '''Create ``markClass`` statements.'''
        txt = ''
        for markName in self.marksDict.keys():
            markClassName = self.makeMarkClassName(markName)
            for markGlyph, markAnchorPos in self.marksDict[markName]:
                txt += 'markClass '
                txt += '[%s] ' % markGlyph
                txt += '<anchor %s %s> ' % markAnchorPos
                txt += '%s;\n' % markClassName
        return txt

    def writeMarkFeature(self):
        '''Create ``mark`` feature code.'''
        txt = 'feature mark {\n\n'
        for markName in self.allMarks:
            lookupName = 'base_%s' % markName
            txt += '\tlookup %s {\n' % lookupName
            for baseGlyph in self.basesDict.keys():
                if markName in self.basesDict[baseGlyph]:
                    markClassName = self.makeMarkClassName(markName)
                    baseAnchorPos = self.basesDict[baseGlyph][markName][0]
                    txt += '\t\tpos base [%s] ' % baseGlyph
                    txt += '<anchor %s %s> ' % baseAnchorPos
                    txt += 'mark %s;\n' % markClassName
            txt += '\t} %s;\n\n' % lookupName
        txt += '} mark;\n'
        return txt

    def writeTableGDEF(self):
        '''Create code for ``GDEF`` table.'''
        txt  = '@allBases = [%s];\n' % ' '.join(self.allBases)
        txt += '@allMarks = [%s];\n' % ' '.join(self.allMarkClasses)
        txt += '\n'
        txt += 'table GDEF {\n'
        txt += '\tGlyphClassDef @allBases,,@allMarks,;\n'
        txt += '} GDEF;\n'
        txt += '\n'
        return txt

    def buildDicts(self):
        '''Transform raw input data into internal data structures.'''

        self.marksDict = {}
        self.basesDict = {}

        for baseGlyph, markGlyphs in self.markToBaseDict.items():

            if not baseGlyph in self.font:
                if self.verbose:
                    print("[PROBLEM] base glyph '%s' not in font '%s'." % (baseGlyph, self.fontName))
                continue

            for markGlyph, anchorName in markGlyphs:

                if markGlyph not in self.font:
                    if self.verbose:
                        print("[PROBLEM] mark glyph '%s' not in font '%s'." % (markGlyph, self.fontName))
                    continue

                # get mark anchor
                markAnchor = [a for a in self.font[markGlyph].anchors if a.name == '_%s' % anchorName]
                if not len(markAnchor):
                    if self.verbose:
                        print("[PROBLEM] mark glyph '%s' has no anchor '_%s'." % (markGlyph, anchorName))
                    continue

                markAnchor = markAnchor[0]
                markAnchorPos = int(markAnchor.position[0]), int(markAnchor.position[1])

                # get base anchor
                baseAnchor = [a for a in self.font[baseGlyph].anchors if a.name == '%s' % anchorName]
                if not len(baseAnchor):
                    if self.verbose:
                        print("[PROBLEM] base glyph '%s' has no anchor '%s'." % (baseGlyph, anchorName))
                    continue

                baseAnchor = baseAnchor[0]
                baseAnchorPos = int(baseAnchor.position[0]), int(baseAnchor.position[1])

                # save mark data
                if anchorName not in self.marksDict:
                    self.marksDict[anchorName] = []

                markItem = markGlyph, markAnchorPos

                if not markItem in self.marksDict[anchorName]:
                    if self.verbose:
                        print("[OK] anchor '%s' %s found in mark glyph '%s'..." % (anchorName, markAnchorPos, markGlyph))
                    self.marksDict[anchorName].append(markItem)

                # save base data
                if baseGlyph not in self.basesDict:
                    self.basesDict[baseGlyph] = {}

                if anchorName not in self.basesDict[baseGlyph]:
                    self.basesDict[baseGlyph][anchorName] = [baseAnchorPos, []]

                if markGlyph not in self.basesDict[baseGlyph][anchorName][1]:
                    if self.verbose:
                        print("[OK] anchor '%s' %s found in mark glyph '%s'..." % (anchorName, baseAnchorPos, baseGlyph))
                    self.basesDict[baseGlyph][anchorName][1].append(markGlyph)

    def compile(self):
        '''
        Compile the available data into ``mark`` feature code.

        '''
        self.buildDicts()
        txt = ''
        txt += self.writeMarkClasses()
        txt += '\n'
        txt += self.writeMarkFeature()
        txt += '\n'
        txt += self.writeTableGDEF()
        return txt

    def write(self, langsystem=True):
        '''
        Write the ``mark`` feature code into the font.
        
        Adds boilerplate ``languagesystem`` statements at the top.

        '''
        txt = ''
        if langsystem:
            txt += 'languagesystem DFLT dflt;\n'
            txt += 'languagesystem latn dflt;\n'
            txt += '\n'
        txt += self.compile()
        self.font.features.text = txt

