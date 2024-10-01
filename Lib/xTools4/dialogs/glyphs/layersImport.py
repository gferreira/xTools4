import ezui


class ImportGlyphsIntoLayerDialog(ezui.WindowController):

    title = 'layers'
    width   = 123
    margins = 10

    def build(self):
        content = """
        (get ufo…)     @getUFO

        source layer
        [_ ...]        @sourceLayer

        target layer
        ( ) font name  @targetLayerMode
        (X) custom
        [__]           @targetLayer

        [X] decompose  @decompose

        (import)       @importButton
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            getUFO=dict(
                width="fill",
            ),
            importButton=dict(
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

    ImportGlyphsIntoLayerDialog()
