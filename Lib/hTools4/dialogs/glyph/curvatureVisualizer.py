import ezui


class CurvatureVisualizerDialog(ezui.WindowController):

    title   = 'curvature'
    width   = 123
    margins = 10

    def build(self):
        content = """
        * ColorWell         @color

        scale
        --X-----            @scale

        steps
        --X-----            @steps

        [X] selection only  @selection
        [X] show preview    @preview
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

    CurvatureVisualizerDialog()
