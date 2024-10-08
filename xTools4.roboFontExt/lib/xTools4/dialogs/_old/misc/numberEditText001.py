import vanilla
from AppKit import NSControlTextDidChangeNotification, NSNotificationCenter, NSTextField
# from lib.tools.debugTools import ClassNameIncrementer

class RFNumberTextField_001(NSTextField): # metaclass=ClassNameIncrementer

    def textView_doCommandBySelector_(self, tv, selector):
        self.succes = False
        self.tryToPerform_with_(selector, tv)
        return self.succes

    def _changeValue_(self, value):
        value = self.floatValue() + value
        self.setObjectValue_(str(round(value, 3)))
        self._postUpdate()
        self.succes = True
        self.delegate().action_(self)

    def _postUpdate(self):
        nc = NSNotificationCenter.defaultCenter()
        nc.postNotificationName_object_(NSControlTextDidChangeNotification, self)

    def moveUp_(self, sender):
        self._changeValue_(0.01)

    def moveUpAndModifySelection_(self, sender):
        self._changeValue_(0.1)

    def moveToBeginningOfDocumentAndModifySelection_(self, sender):
        self._changeValue_(1.0)

    def moveDown_(self, sender):
        self._changeValue_(-0.01)

    def moveDownAndModifySelection_(self, sender):
        self._changeValue_(-0.1)

    def moveToEndOfDocumentAndModifySelection_(self, sender):
        self._changeValue_(-1.0)

    def insertNewline_(self, sender):
        if hasattr(self, "_enterCallback"):
            self._enterCallback(self)

class BaseNumberEditText_001(vanilla.EditText):

    nsTextFieldClass = RFNumberTextField_001

    def __init__(self, *args, **kwargs):
        self._enterCallback = kwargs.get("enterCallback")
        if self._enterCallback:
            del kwargs["enterCallback"]
        super(BaseNumberEditText_001, self).__init__(*args, **kwargs)
        self.getNSTextField()._enterCallback = self._baseEnterCallback

    def _baseEnterCallback(self, sender):
        if self._enterCallback:
            self._enterCallback(self)

class NumberEditText_001(BaseNumberEditText_001):

    def __init__(self, posSize, text="", sizeStyle="regular", callback=None, allowFloat=True, allowNegative=True, allowEmpty=True, minimum=None, maximum=None, decimals=2, formatter=None, continuous=True):
        super(NumberEditText_001, self).__init__(posSize, text="", callback=self._entryCallback, sizeStyle=sizeStyle, continuous=continuous)
        self._finalCallback = callback
        self._allowFloat = allowFloat
        self._allowNegative = allowNegative
        self._allowEmpty = allowEmpty
        self._minimum = minimum
        self._maximum = maximum
        self._numberStringFormat = "%i"
        if allowFloat:
            self._numberStringFormat = "%%.%df" % decimals
        if allowFloat:
            self._numberClass = float
        else:
            self._numberClass = int
        self._previousString = None
        self.set(text)

    def _numberToString(self, value):
        return self._numberStringFormat % value

    def _stringToNumber(self, string):
        value = None
        newString = string
        try:
            value = self._numberClass(string)
            if value < 0 and not self._allowNegative:
                newString = self._previousString
                value, n = self._stringToNumber(newString)
            if self._minimum is not None and value < self._minimum:
                value = self._minimum
                newString = self._numberToString(value)
            if self._maximum is not None and value > self._maximum:
                value = self._maximum
                newString = self._numberToString(value)
        except (ValueError, TypeError):
            value = None
            if string == "":
                pass
            elif string == "-" and self._allowNegative:
                pass
            elif string == "." and self._allowFloat:
                pass
            elif string == "-." and self._allowFloat and self._allowNegative:
                pass
            else:
                newString = self._previousString
        # handle -0.0
        if value == 0:
            value = 0
        if not self._allowEmpty and value is None:
            if self._minimum is not None:
                value = self._minimum
            else:
                value = 0
            newString = self._numberToString(value)
        return value, newString

    def _entryCallback(self, sender):
        oldString = super(NumberEditText_001, self).get()
        value, newString = self._stringToNumber(oldString)
        self._previousString = newString
        if newString != oldString:
            super(NumberEditText_001, self).set(newString)
        if self._finalCallback is not None:
            self._finalCallback(sender)

    def get(self):
        string = super(NumberEditText_001, self).get()
        return self._stringToNumber(string)[0]

    def set(self, value):
        if value is None:
            self._previousString = ""
        else:
            self._previousString = value
        if value == "":
            value = None
        if isinstance(value, str):
            if self._allowFloat:
                value = float(value)
            else:
                value = int(value)
        if value is not None:
            if value < 0 and not self._allowNegative:
                value = abs(value)
            value = self._numberToString(value)
        elif value is None and not self._allowEmpty:
            if self._minimum is not None:
                value = self._minimum
            else:
                value = 0
            value = self._numberToString(value)
        super(NumberEditText_001, self).set(value)

if __name__ == '__main__':

    def callback(sender):
        print(sender.get())
    
    w = vanilla.Window((150, 40))
    w.edit = NumberEditText_001((10, 10, -10, 22), text='100.0', callback=callback, continuous=False)
    w.open()
