import ezui


class CreateAnchorsDialog(ezui.WindowController):

    title   = "anchors"
    width   = 123
    margins = 10

    def build(self):
        content = """
        name 
        [__]           @anchorName

        y pos 
        [__](±)        @posY
        [_ ...]        @reference

        x alignment
        [_ ...]        @layerTarget

        [X] overwrite  @overwrite

        (create)       @applyButton

        [ ] preview    @preview
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

    CreateAnchorsDialog()
