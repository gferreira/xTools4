import ezui


class CondenseGlyphsDialog(ezui.WindowController):

    title   = 'condense'
    width   = 123
    margins = 10

    def build(self):
        content = """
        regular
        [_ ...]      @regular

        bold
        [_ ...]      @bold

        factor
        [__](±)      @factor

        (apply)      @applyButton

        [ ] preview  @preview
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

    CondenseGlyphsDialog()
