from PyQt5.QtWidgets import QTextEdit


def createPart(ctx, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partName'])

    # Create the QProgressBar widget and set its orientation to vertical
    widget = QTextEdit(ctx.window)

    # Get the path of the selected file
    file_path = "..\\Models\\NewDuck.json"

    # Load the contents of the file into the code editor
    with open(file_path, 'r') as f:
        file_contents = f.read()
    widget.setPlainText(file_contents)

    # Display the progress bar
    me['qtWidget'] = widget
    widget.show()


def setFocus(ctx, me):
    print('Set Focus:', me['label'])
