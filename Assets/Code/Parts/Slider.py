from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QProgressBar, QSlider
from PyQt5.QtCore import Qt

class FontSizeSlider(QSlider):
    def __init__(self, window):
        super().__init__(Qt.Horizontal, window)

        self.setRange(7, 36)
        self.setValue(16)

        self.window = window
        self.valueChanged.connect(self.handle_value_changed)

    def handle_value_changed(self, value):
        print(f"Slider value changed to {value}")
        me = self.window.getPart("Text Editor")
        if me != None:
            widget = self.window.getMEData(me, 'qtWidget')
            font = QFont('Arial', value)
            widget.setFont(font)

def createPart(window, me):
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is not None:
        return

    print('create Part: ', me['partType'])

    # Create the QProgressBar widget and set its orientation to vertical
    slider = FontSizeSlider(window)

    # Display the progress bar
    slider.show()

    window.setMEData(me, 'qtWidget', slider)


def setFocus(ctx, me):
    print('Set Focus:', me['label'])
