import ezui


class MaskDialog(ezui.WindowController):

    title   = 'mask'
    width   = 123
    margins = 10

    def build(self):
        content = """
        main layer
        [_ ...]         @sourceLayer

        mask layer
        [_ ...]         @maskLayers

        (copy)          @copyButton
        (flip)          @flipButton
        (clear)         @clearButton

        [X] copy width  @copyWidth
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small",
            ),
            copyButton=dict(
                width="fill",
            ),
            flipButton=dict(
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

    MaskDialog()
