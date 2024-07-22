import ezui


class MeasureHandlesTool(ezui.WindowController):

    title   = 'measure'
    width   = 123
    margins = 10

    def build(self):
        content = """
        (X) length         @captionMode
        ( ) angle

        [X] handles        @handlesShow
        * ColorWell        @handlesColor

        [X] line segments  @linesShow
        * ColorWell        @linesColor

        caption size
        --X-----           @captionSize

        [X] show preview   @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
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

    MeasureHandlesTool()
