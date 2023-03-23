from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit

def showFile(widget, path):
    # Load the contents of the file into the code editor
    with open(path, 'r') as f:
        file_contents = f.read()
    widget.setPlainText(file_contents)

def createPart(window, me):
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is not None:
        return

    print('create Part: ', me['partType'])

    # Create the QProgressBar widget and set its orientation to vertical
    widget = QTextEdit(window)
    font = QFont('Arial', 18)
    widget.setFont(font)

    # Get the path of the selected file
    showFile(widget, "..\\Models\\NewDuck.json")


    # Display the progress bar
    window.setMEData(me, 'qtWidget', widget)

    if 'partName' in me:
        window.registerPart(me, me['partName'])

    widget.show()


def setFocus(window, me):
    print('Set Focus:', me['label'])
