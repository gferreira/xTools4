import ezui


class GlyphActionsDialog(ezui.WindowController):

    title   = 'actions'
    width   = 123
    margins = 10

    actions = [
        'balance handles',
        'decompose',
        'remove overlaps',
        'add extreme points',
        'auto starting points',
        'auto contour direction',
        'round to integer',
    ]

    def build(self):
        content = """
        |---|        @actions
        (apply)      @applyButton
        [X] preview  @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            actions=dict(
                height=200,
                items=self.actions,
                alternatingRowColors=True,
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

    GlyphActionsDialog()
