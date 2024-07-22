import ezui


class ShiftPointsDialog(ezui.WindowController):

    title   = 'shift'
    width   = 123
    margins = 10

    def build(self):
        content = """
        pos
        [__](±)      @pos

        axis
        (X) x        @axis
        ( ) y

        side
        (X) -        @side
        ( ) +

        delta
        [__](±)      @delta

        shift
        ( ) -        @shift
        (X) +

        (apply)      @apply

        [X] preview  @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            )
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

    ShiftPointsDialog()
