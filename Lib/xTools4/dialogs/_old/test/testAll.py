from hTools3.dialogs import hDialog

class TestAllDialog(hDialog):

    title = 'test all'

    def __init__(self):
        self.height = 400
        self.w = self.window((self.width, self.height), self.title)
        self.w.open()

if __name__ == "__main__":

    TestAllDialog()
