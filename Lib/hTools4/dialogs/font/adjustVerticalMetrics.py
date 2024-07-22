import ezui


class AdjustVerticalMetricsDialog(ezui.WindowController):

    title    = "dimensions"
    width    = 123
    margins  = 10

    def build(self):
        content = """
        xHeight
        [__](±)     @xHeight

        ascender
        [__](±)     @ascender

        descender
        [__](±)     @descender

        capHeight
        [__](±)     @capHeight

        unitsPerEm
        [__](±)     @unitsPerEm

        italicAngle
        [__](±)     @italicAngle
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
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

    AdjustVerticalMetricsDialog()
