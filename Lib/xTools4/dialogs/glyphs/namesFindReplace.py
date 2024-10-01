import ezui


class FindReplaceGlyphNamesDialog(ezui.WindowController):

    title   = 'replace'
    width   = 123
    margins = 10

    def build(self):
        content = """
        find
        [__]           @find

        replace
        [__]           @replace

        (apply)        @applyButton

        [X] overwrite  @overwrite
        [X] duplicate  @duplicate
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

    FindReplaceGlyphNamesDialog()
