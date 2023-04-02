import os

from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QPlainTextEdit, QSplitter, QListWidgetItem

import CodeHilighter


class EditorFrame(QWidget):
    def __init__(self, window, dirPath):
        super().__init__(window)

        self.dirPath = dirPath
        self.curFile = None

        self.font = QFont("Arial", 16)

        # Create widgets
        self.title_label = QLabel('Title', self)
        self.title_label.setFont(self.font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
                "background-color: blue;"
                "border: 2px solid white;"
                "color: yellow;"
                "font-size: 12pt;"
                "margin: 1px;"
            )

        # Create the list widget
        self.list_widget = QListWidget(self)
        self.list_widget.setFont(self.font)
        self.list_widget.currentItemChanged.connect(self.fileChanged)

        # Create the text editor widget
        self.editor_widget = QPlainTextEdit(self)
        self.editor_widget.setFont(self.font)
        self.editor_widget.setStyleSheet("background-color: white; color: black;")
        self.editor_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.editor_widget.hilighter = CodeHilighter.PythonHighlighter(self.editor_widget.document())

        # Create splitter
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.addWidget(self.list_widget)
        self.splitter.addWidget(self.editor_widget)

        self.title_label.show()
        self.splitter.show()

        self.dragging = False

        self.populateFileList(dirPath)
        self.list_widget.setCurrentRow(0)
        # self.showFile(self.curFile)

    def fileChanged(self, current, previous):
        if current is not None:
            self.showFile(current.text())

    def showFile(self, fileName):
        filePath = self.dirPath + '/' + fileName
        with open(filePath, 'r') as pythonFile:
            title = f'Part: {fileName} (Dir: {self.dirPath}'
            self.title_label.setText(title)
            fileData = pythonFile.read()
            self.editor_widget.setPlainText(fileData)

    def populateFileList(self, dirpath):
        # Clear the existing items in the model
        self.list_widget.clear()

        # Iterate through the directory and add .py files to the tree
        for filename in os.listdir(dirpath):
            if filename.endswith('.py'):
                # Create a new item for the .py file
                file_info = QFileInfo(os.path.join(dirpath, filename))
                item = QListWidgetItem(file_info.fileName())
                self.list_widget.addItem(item)

    def resizeEvent(self, event):
        size = event.size()

        self.title_label.setGeometry(0,0, size.width(), 30)
        self.splitter.setGeometry(0,30, size.width(), size.height() - 30)

def createPart(window, me):
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is not None:
        return

    print('create Part: ', me['partType'])

    # The list if populated from this dir
    dirPath = me['dirPath']
    widget = EditorFrame(window, dirPath)
    window.setMEData(me, 'qtWidget', widget)
    if 'partName' in me:
        window.registerPart(me, me['partName'])

    widget.show()

def setFocus(window, me):
    print('Set Focus:', me['label'])
