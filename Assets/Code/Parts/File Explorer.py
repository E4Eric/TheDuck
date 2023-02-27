import os
from PyQt5.QtWidgets import QTreeView, QFileSystemModel

def createPart(ctx, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partName'])

    # Create a tree view
    tree_view = QTreeView(ctx.window)
    tree_view.setRootIsDecorated(False)
    tree_view.setAlternatingRowColors(True)

    # Set the model of the tree view
    file_system_model = QFileSystemModel()
    file_system_model.setRootPath(os.path.expanduser("~"))
    tree_view.setModel(file_system_model)
    tree_view.setRootIndex(file_system_model.index(os.path.expanduser("~")))

    me['qtWidget'] = tree_view


def setFocus(ctx, me):
    print('Set Focus:', me['label'])
