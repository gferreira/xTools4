import ezui


class PrintGlyphNamesDialog(ezui.WindowController):

    title   = 'print'
    width   = 123
    margins = 10

    def build(self):
        content = """
        glyph mode
        (X) glyph names    @glyphMode
        ( ) unicode chars

        print mode
        (X) plain string   @printMode
        ( ) plain list
        ( ) Python string
        ( ) Python list

        (print)            @printButton

        [X] sorted         @sorted
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small",
            ),
            printButton=dict(
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

    PrintGlyphNamesDialog()
