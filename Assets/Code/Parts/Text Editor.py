from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTextEdit

def showFile(widget, path):
    # Load the contents of the file into the code editor
    with open(path, 'r') as f:
        file_contents = f.read()
    widget.setPlainText(file_contents)

def createPart(ctx, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partType'])

    # Create the QProgressBar widget and set its orientation to vertical
    widget = QTextEdit(ctx.window)
    font = QFont('Arial', 14)
    widget.setFont(font)

    # Get the path of the selected file
    showFile(widget, "..\\Models\\NewDuck.json")


    # Display the progress bar
    me['qtWidget'] = widget
    if 'partName' in me:
        ctx.registerPart(me, me['partName'])

    widget.show()


def setFocus(ctx, me):
    print('Set Focus:', me['label'])
