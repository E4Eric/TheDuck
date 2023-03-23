from PyQt5.QtWidgets import QDial


def createPart(window, me):
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is None:
        return

    print('create Part: ', me['partType'])

    # Create the QProgressBar widget and set its orientation to vertical
    dial = QDial(window)
    dial.setRange(0, 100)
    dial.setValue(50)

    # Display the progress bar
    dial.show()

    window.setMEData(me,  'tWidget', dial)

def setFocus(ctx, me):
    print('Set Focus:', me['label'])
