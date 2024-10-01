import ezui


class CopyMarginsDialog(ezui.WindowController):

    title   = 'margins'
    width   = 123
    margins = 10

    def build(self):
        content = """
        source
        [_ ...]    @source

        target
        [_ ...]    @target
        [_ ...]    @targetLayer

        [X] left   @sides
        [X] right

        (copy)     @copyButton
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
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


if __name__ == '__main__':

    CopyMarginsDialog()

