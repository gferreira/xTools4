import ezui


class ExportLayersDialog(ezui.WindowController):

    title   = 'layers'
    width   = 123
    margins = 10

    def build(self):
        content = """
        no font open       @fontName
        |---|              @layers

        (export)           @exportButton

        [X] overwrite ufo  @overwrite
        [X] open font      @openFont
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            layers=dict(
                height=100,
                alternatingRowColors=True,
            ),
            exportButton=dict(
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

    ExportLayersDialog()
