from PyQt5.QtWidgets import QDial


def createPart(ctx, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partType'])

    # Create the QProgressBar widget and set its orientation to vertical
    dial = QDial(ctx.window)
    dial.setRange(0, 100)
    dial.setValue(50)

    # Display the progress bar
    dial.show()

    me['qtWidget'] = dial


def setFocus(ctx, me):
    print('Set Focus:', me['label'])
