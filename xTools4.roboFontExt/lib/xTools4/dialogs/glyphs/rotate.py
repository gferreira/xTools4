import ezui


class RotateGlyphsDialog(ezui.WindowController):

    title   = "rotate"
    width   = 123
    margins = 10

    def build(self):
        content = """
        * ImageButtonGrid        @imageButtonGrid
        > * ImageButtonGridRow
        >> ({circle})            @upLeftButton
        >> ({circle})            @upCenterButton
        >> ({circle})            @upRightButton
        > * ImageButtonGridRow
        >> ({circle})            @centerLeftButton
        >> ({circle})            @centerButton
        >> ({circle})            @centerRightButton
        > * ImageButtonGridRow
        >> ({circle})            @downLeftButton
        >> ({circle})            @downCenterButton
        >> ({circle})            @downRightButton

        angle
        [__](±)                  @angle

        (apply)                  @applyButton

        [X] preview              @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            imageButtonGrid=dict(
                sizeStyle="regular",
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

    RotateGlyphsDialog()
