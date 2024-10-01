import ezui


class ClearFontDataDialog(ezui.WindowController):

    title   = 'clear'
    width   = 123
    margins = 10

    def build(self):
        content = """
        [ ] guidelines       @options
        [ ] groups
        [ ] kerning
        [ ] features
        [ ] stems
        [ ] blue values
        [ ] layers
        [ ] template glyphs
        [ ] mark colors

        (clear)              @clearButton
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
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


if __name__ == '__main__':

    ClearFontDataDialog()
