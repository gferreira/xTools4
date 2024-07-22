import ezui


class LinkPointsTool(ezui.WindowController):

    title   = "links"
    width   = 123
    margins = 10

    def build(self):
        content = """
        (X) length        @captionMode
        ( ) angle

        (link)            @linkButton
        (unlink)          @unlinkButton

        * ColorWell       @color

        caption size
        --X-----          @captionSize

        [ ] projections   @projections

        (clear all)       @clearButton

        [X] show preview  @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            clearButton=dict(
                width="fill",
            ),
            linkButton=dict(
                width="fill",
            ),
            unlinkButton=dict(
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

    LinkPointsTool()
