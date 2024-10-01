import ezui


class MarkGlyphTypesDialog(ezui.WindowController):

    title = 'mark'
    width   = 123
    margins = 10

    def build(self):
        content = """
        [X] contours    @contours
        * ColorWell     @colorContours

        [X] components  @components
        * ColorWell     @colorComponents

        [X] mixed       @mixed
        * ColorWell     @colorMixed

        [X] empty       @empty
        * ColorWell     @colorEmpty

        (apply)         @applyButton
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


if __name__ == '__main__':

    MarkGlyphTypesDialog()
