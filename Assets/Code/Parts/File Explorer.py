import os

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QTextEdit


class FileExplorer(QTreeView):
    def __init__(self, ctx, parent=None):
        super().__init__(parent)

        self.ctx = ctx

    def mouseDoubleClickEvent(self, event):
        index = self.indexAt(event.pos())
        model = self.model()
        item_data = model.data(index)
        path = model.filePath(index)
        if path.endswith('.py') or path.endswith('.json'):
            me = self.ctx.getPart("Text Editor")
            if me != None:
                widget = me['qtWidget']
                with open(path, 'r') as f:
                    file_contents = f.read()
                # widget.setSyntaxHighlighter(QTextEdit.SyntaxHighlighter.Python)
                widget.setPlainText(file_contents)

        else:
            print("Double clicked on file:", path)
            super().mouseDoubleClickEvent(event)

    def on_double_clicked(self, index: QModelIndex, event):
        # Get the model associated with the view
        model = self.model()
        # Retrieve the item's data using the index
        item_data = model.data(index)
        # Get the path of the item
        path = model.filePath(index)
        # Check if the item is a directory
        is_dir = model.isDir(index)
        # Handle double click event
        if is_dir:
            # Forward the event to the parent class
            super().mouseDoubleClickEvent(event)
        else:
            print("Double clicked on file:", item_data)
            # Do something with the file

def createPart(ctx, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partType'])

    # Create a tree view
    widget = FileExplorer(ctx, ctx.window)
    font = QFont('Arial', 14)
    widget.setFont(font)

    widget.setRootIsDecorated(False)
    widget.setAlternatingRowColors(True)

    # Set the model of the tree view
    file_system_model = QFileSystemModel()
    rootPath = "../.."
    file_system_model.setRootPath(rootPath)
    widget.setModel(file_system_model)
    widget.setRootIndex(file_system_model.index(rootPath))

    me['qtWidget'] = widget


def setFocus(ctx, me):
    print('Set Focus:', me['label'])
