import ezui


class MoveGlyphsDialog(ezui.WindowController):

    title   = "move"
    width   = 123
    margins = 10

    def build(self):
        content = """
        x delta
        [__](±)      @deltaX

        y delta
        [__](±)      @deltaY

        (apply)      @applyButton

        [X] preview  @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            applyButton=dict(
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

    MoveGlyphsDialog()
