import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeView, QFileSystemModel

class FileBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Browser")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        # Create a tree view
        self.tree_view = QTreeView()
        self.tree_view.setRootIsDecorated(False)
        self.tree_view.setAlternatingRowColors(True)

        # Set the model of the tree view
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath(os.path.expanduser("~"))
        self.tree_view.setModel(self.file_system_model)
        self.tree_view.setRootIndex(self.file_system_model.index(os.path.expanduser("~")))

        layout.addWidget(self.tree_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileBrowser()
    window.show()
    sys.exit(app.exec_())
