import ezui


class DuplicateRenameGlyphsDialog(ezui.WindowController):

    title   = 'duplicate glyphs'
    width   = 123*3
    margins = 10

    def build(self):
        content = """
        (add current font selection)     @addSelectionButton
        (import glyph names from file…)  @importGlyphNamesButton

        |----------|-----------|
        | original | duplicate |         @glyphNames
        |----------|-----------|
        > (+-)                           @glyphNamesAddRemoveButton
        > (select all)                   @glyphNamesSelectAllButton

        (export glyph names to file…)    @exportGlyphNamesButton
        (duplicate glyphs)               @duplicateGlyphsButton

        [ ] preflight                    @preflight
        [ ] overwrite existing glyphs    @overwrite
        [ ] mark duplicates              @markDuplicates

        * ColorWell                      @markColor
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            glyphNames=dict(
                height=200,
                alternatingRowColors=True,
                columnDescriptions=[
                    dict(
                        identifier="original",
                        title="original",
                        editable=True
                    ),
                    dict(
                        identifier="duplicate",
                        title="duplicate",
                        editable=True
                    ),
                ],
            ),
            addSelectionButton=dict(
                width="fill",
            ),
            importGlyphNamesButton=dict(
                width="fill",
            ),
            exportGlyphNamesButton=dict(
                width="fill",
            ),
            duplicateGlyphsButton=dict(
                width="fill",
            ),
        )
        self.w = ezui.EZPanel(
            title=self.title,
            content=content,
            descriptionData=descriptionData,
            controller=self,
            margins=self.margins,
            size=(self.width, 'auto'),
        )

    def started(self):
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()


    # def __init__(self):
    #     self.height  = self.buttonHeight * 6
    #     self.height += self.textHeight * 12
    #     self.height += self.padding * 10
    #     self.w = self.window((self.width * 3, self.height), self.title)

    #     x = y = p = self.padding
    #     self.w.addSelectionToList = SquareButton(
    #             (x, y, -p, self.buttonHeight),
    #             'add current font selection',
    #             callback=self.addSelectionToListCallback,
    #             sizeStyle=self.sizeStyle)

    #     y += self.buttonHeight + p
    #     self.w.importGlyphNames = SquareButton(
    #             (x, y, -p, self.buttonHeight),
    #             'import glyph names from file…',
    #             callback=self.importGlyphNamesCallback,
    #             sizeStyle=self.sizeStyle)

    #     y += self.buttonHeight + p
    #     textBoxHeight = self.textHeight * 8
    #     self.w.glyphNames = List(
    #             (x, y, -p, textBoxHeight),
    #             [],
    #             enableDelete=True,
    #             drawFocusRing=False,
    #             columnDescriptions=[
    #                 dict(title='original',  editable=True, allowsSorting=True),
    #                 dict(title='duplicate', editable=True, allowsSorting=True),
    #             ],
    #         )

    #     y += textBoxHeight + p
    #     self.w.addEntry = SquareButton(
    #             (x, y, -p, self.buttonHeight),
    #             'add new entry',
    #             callback=self.addNewEntryCallback,
    #             sizeStyle=self.sizeStyle)

    #     y += self.buttonHeight + p
    #     self.w.selectAllGlyphNames = CheckBox(
    #             (x, y, -p, self.textHeight),
    #             'select all',
    #             value=False,
    #             callback=self.selectAllGlyphNamesCallback,
    #             sizeStyle=self.sizeStyle)

    #     y += self.textHeight + p
    #     self.w.exportGlyphNames = SquareButton(
    #             (x, y, -p, self.buttonHeight),
    #             'export glyph names to file…',
    #             callback=self.exportGlyphNamesCallback,
    #             sizeStyle=self.sizeStyle)

    #     y += self.buttonHeight + p
    #     self.w.duplicateAndRename = SquareButton(
    #             (x, y, -p, self.buttonHeight),
    #             "duplicate glyphs",
    #             callback=self.duplicateAndRenameCallback,
    #             sizeStyle=self.sizeStyle)

    #     y += self.buttonHeight + p
    #     self.w.preflight = CheckBox(
    #             (x, y, -p, self.textHeight),
    #             'preflight',
    #             value=False,
    #             sizeStyle=self.sizeStyle)

    #     y += self.textHeight
    #     self.w.overwrite = CheckBox(
    #             (x, y, -p, self.textHeight),
    #             'overwrite existing glyphs',
    #             value=False,
    #             sizeStyle=self.sizeStyle)

    #     y += self.textHeight
    #     self.w.markGlyphs = CheckBox(
    #             (x, y, -p, self.textHeight),
    #             'mark duplicates',
    #             value=False,
    #             sizeStyle=self.sizeStyle)

    #     y += self.textHeight + p
    #     nsColor = rgb2nscolor((0, 0.5, 1, 0.5))
    #     self.w.markColor = ColorWell(
    #             (x, y, -p, self.buttonHeight),
    #             color=nsColor)

    #     self.w.open()


if __name__ == '__main__':

    DuplicateRenameGlyphsDialog()
