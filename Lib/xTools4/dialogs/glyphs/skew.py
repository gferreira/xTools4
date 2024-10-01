import ezui


class SkewGlyphsDialog(ezui.WindowController):

    title = 'skew'
    width   = 123
    margins = 10

    def build(self):
        content = """
        angle
        [__](±)              @angleValue

        origin
        [__](±)              @originValue

        [X] set slant angle  @setSlantAngle

        (apply)              @applyButton

        [X] preview          @preview
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

    SkewGlyphsDialog()
