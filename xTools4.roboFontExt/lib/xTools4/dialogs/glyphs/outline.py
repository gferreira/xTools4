import ezui


class OutlineGlyphsDialog(ezui.WindowController):

    title = 'outline'

    width   = 123
    margins = 10

    def build(self):
        content = """
        source layer
        [_ ...]      @source

        target layer
        [_ ...]      @target

        stroke
        [__](±)      @stroke

        join style
        (X) square   @joinStyle
        ( ) round
        ( ) butt

        cap style
        (X) square   @capStyle
        ( ) round
        ( ) butt

        edges        @edges
        [X] inner
        [X] outer

        (apply)      @applyButton

        [X] preview  @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small",
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

    OutlineGlyphsDialog()
