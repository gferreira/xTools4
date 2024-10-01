import ezui


class FindGlyphComponentsDialog(ezui.WindowController):

    title   = "components"
    width   = 123
    margins = 10

    def build(self):
        content = """
        find
        [__]         @baseGlyph

        |---|        @composedGlyphs

        * ColorWell  @color
        (mark)       @markButton

        [__]         @newBaseGlyph
        (replace)    @replaceButton
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            composedGlyphs=dict(
                height=100,
                alternatingRowColors=True,
            ),
            markButton=dict(
                width="fill",
            ),
            replaceButton=dict(
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


if __name__ == '__main__':

    FindGlyphComponentsDialog()
