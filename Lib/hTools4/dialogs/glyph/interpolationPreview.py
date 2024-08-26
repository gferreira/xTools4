import ezui


class InterpolationPreviewDialog_EZUI(ezui.WindowController):

    title   = 'interpolation'
    width   = 123
    margins = 10

    def build(self):
        content = """
        [_ ...]           @font2
        [_ ...]           @fontLayers
        [__]              @otherGlyph

        --X-----          @steps

        * ColorWell       @color

        [X] show lines    @showLines
        [X] show steps    @showSteps
        [X] align center  @alignCenter
        [X] show preview  @showPreview

        ----------------------------------

        starting point
        ((( ← | → )))     @startingPoint

        contour index
        ((( ← | → )))     @contourIndex
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            startingPoint=dict(
                sizeStyle="regular",
                width="fill",
            ),
            contourIndex=dict(
                sizeStyle="regular",
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

    InterpolationPreviewDialog_EZUI()
