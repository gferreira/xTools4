import ezui


class CopyWidthDialog(ezui.WindowController):

    title = 'width'
    width   = 123
    margins = 10

    def build(self):
        content = """
        source
        [_ ...]    @sourceFont

        target
        [_ ...]    @targetFont
        |-----|    @targetLayers

        (copy)     @copyButton
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            targetLayers=dict(
                height=60,
                alternatingRowColors=True,
            ),
            copyButton=dict(
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

    CopyWidthDialog()
