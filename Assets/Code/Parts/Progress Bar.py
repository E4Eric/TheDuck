from PyQt5.QtWidgets import QApplication, QProgressBar
from PyQt5.QtCore import Qt


def createPart(window, me):
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is None:
        return

    print('create Part: ', me['partType'])

    # Create the QProgressBar widget and set its orientation to vertical
    progress_bar = QProgressBar(window)
    progress_bar.setOrientation(Qt.Vertical)

    # Set the minimum and maximum values of the progress bar
    progress_bar.setMinimum(0)
    progress_bar.setMaximum(100)

    # Set the current value of the progress bar
    progress_bar.setValue(50)

    # Display the progress bar
    progress_bar.show()

    window.setMEData(me, 'qtWidget', progress_bar)

def setFocus(ctx, me):
    print('Set Focus:', me['label'])
