import ezui


class SelectLayersDialog(ezui.WindowController):

    title      = "layers"
    width   = 123
    margins = 10

    def build(self):
        content = """
        /(font name)  @fontName
        |---|         @layers
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small",
            ),
            layers=dict(
                height=200,
                alternatingRowColors=True,
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

    SelectLayersDialog()
