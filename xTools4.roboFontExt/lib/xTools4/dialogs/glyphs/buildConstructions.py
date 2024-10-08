import ezui


class BuildConstructionDialog(ezui.WindowController):

    title   = 'constructions'
    width   = 123
    margins = 10

    def build(self):
        content = """
        (load…)  @loadButton
        (edit…)  @editButton
        (save)   @saveButton
        (build)  @buildButton

        [X] preview  @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            loadButton=dict(
                width="fill",
            ),
            editButton=dict(
                width="fill",
            ),
            saveButton=dict(
                width="fill",
            ),
            buildButton=dict(
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

    BuildConstructionDialog()
