from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QProgressBar, QSlider
from PyQt5.QtCore import Qt

class FontSizeSlider(QSlider):
    def __init__(self, ctx, orientation, parent):
        super().__init__(orientation, parent)

        self.ctx = ctx
        self.valueChanged.connect(self.handle_value_changed)

    def handle_value_changed(self, value):
        print(f"Slider value changed to {value}")
        me = self.ctx.getPart("Text Editor")
        if me != None:
            widget = me['qtWidget']
            font = QFont('Arial', value)
            widget.setFont(font)

def createPart(ctx, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partType'])

    # Create the QProgressBar widget and set its orientation to vertical
    slider = FontSizeSlider(ctx, Qt.Horizontal, ctx.window)
    slider.setRange(7, 36)
    slider.setValue(16)

    # Display the progress bar
    slider.show()

    me['qtWidget'] = slider


def setFocus(ctx, me):
    print('Set Focus:', me['label'])
