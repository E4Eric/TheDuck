from PyQt5.QtWidgets import QApplication, QProgressBar, QSlider
from PyQt5.QtCore import Qt


def createPart(ctx, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partName'])

    # Create the QProgressBar widget and set its orientation to vertical
    slider = QSlider(Qt.Horizontal, ctx.window)
    slider.setRange(0, 100)
    slider.setValue(50)

    # Display the progress bar
    slider.show()

    me['qtWidget'] = slider


def setFocus(ctx, me):
    print('Set Focus:', me['label'])
