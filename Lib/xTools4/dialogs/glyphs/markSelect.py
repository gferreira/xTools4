import ezui


class MarkGlyphsDialog(ezui.WindowController):

    title   = 'mark'
    width   = 123
    margins = 10

    def build(self):
        content = """
        (get)        @getButton
        (random)     @randomButton
        * ColorWell  @colorButton
        (set)        @setButton
        (select)     @selectButton
        (clear)      @clearButton
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            getButton=dict(
                width="fill",
            ),
            randomButton=dict(
                width="fill",
            ),
            setButton=dict(
                width="fill",
            ),
            selectButton=dict(
                width="fill",
            ),
            clearButton=dict(
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


if __name__ == "__main__":

    MarkGlyphsDialog()
