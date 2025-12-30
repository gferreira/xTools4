import ezui


KEY = 'com.xTools4.dialogs.variable.roundingBatch'


class RoundingBatchController(ezui.WindowController):

    title = 'BatchRounding'
    key = KEY
    buttonWidth = 80

    content = """
    |-------| @sources
    |       |
    |-------|

    =============

    ( designspace… ) @loadDesignspaceButton
    ( rounding… )    @loadRoundingButton
    ( apply )        @applyButton

    """

    descriptionData = dict(
        loadButton=dict(
            width=buttonWidth,
        ),
        applyButton=dict(
            width=buttonWidth,
        ),
    )

    def build(self):
        self.w = ezui.EZPanel(
            title=self.title,
            content=self.content,
            descriptionData=self.descriptionData,
            controller=self,
            size=(360, 300),
        )
        self.w.workspaceWindowIdentifier = self.title
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.workspaceWindowIdentifier = KEY
        self.w.open()

    def started(self):
        pass

    def destroy(self):
        pass


if __name__ == '__main__':

    OpenWindow(RoundingBatchController)



