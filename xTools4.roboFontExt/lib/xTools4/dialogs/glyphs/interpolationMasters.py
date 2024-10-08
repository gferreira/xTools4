import ezui


class InterpolateGlyphsDialog(ezui.WindowController):

    title   = 'interpolate'
    width   = 123
    margins = 10

    def build(self):
        content = """
        master 1
        [_ ...]           @master1
        [_ ...]           @layer1

        master 2
        [_ ...]           @master2
        [_ ...]           @layer2

        target
        [_ ...]           @layerTarget

        x factor
        [__](±)           @xFactor

        y factor
        [__](±)           @yFactor

        [ ] proportional  @proportional

        (interpolate)     @interpolateButton

        [ ] preview       @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            interpolateButton=dict(
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
    
    InterpolateGlyphsDialog()
