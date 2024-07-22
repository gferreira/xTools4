import ezui


class SetMarginsDialog(ezui.WindowController):

    title   = 'margins'
    width   = 123
    margins = 10

    def build(self):
        content = """
        left
        (X) /=          @leftMode
        ( ) +
        ( ) /-
        [__](±)         @leftValue

        right
        (X) /=          @rightMode
        ( ) +
        ( ) /-
        [__](±)         @rightValue

        [ ] use beam    @beam
        [__](±)         @beamValue

        [X] left        @sides
        [X] right

        (apply)         @applyButton

        [X] preview     @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small",
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
        self.w.getItem('beamValue').enable(False)
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()


if __name__ == "__main__":

    SetMarginsDialog()
