import ezui


class SetGlyphOrderDialog(ezui.WindowController):

    title   = 'font'
    width   = 123
    margins = 10

    def build(self):
        content = """
        (select…)          @getFileButton
        (set glyph order)  @setGlyphOrderButton
        [X] create groups  @createGroupsButton
        [X] paint groups   @paintGroupsButton
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            getFileButton=dict(
                width="fill",
            ),
            setGlyphOrderButton=dict(
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

    SetGlyphOrderDialog()
