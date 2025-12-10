import ezui


KEY = 'com.xTools4.tempEdit'


class TempEditController(ezui.WindowController):

    title      = 'TempEdit'
    key        = KEY
    width      = 123*3
    height     = 640
    lineHeight = 22

    def build(self):
        content = """
        * Accordion: designspaces @designspacesPanel
        > | | @designspaces
        * Accordion: sources @sourcesPanel
        > | | @sources
        * Accordion: glyphs @glyphsPanel
        > | | @glyphNames
        """
        descriptionData = dict(
            designspaces=dict(
                height=self.lineHeight*5,
            ),
            sources=dict(
                height=self.lineHeight*5,
            ),
            glyphNames=dict(
                height=self.lineHeight*5,
            ),

        )
        self.w = ezui.EZPanel(
            title=self.title,
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(self.width, self.height),
            minSize=(self.width*0.9, self.width*0.5),
        )
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.getItem("designspaces").getNSTableView().setRowHeight_(17)
        self.w.workspaceWindowIdentifier = KEY
        self.w.open()



if __name__ == '__main__':

    TempEditController()

