import json

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget

from TheDuck.PythonQt5Impl.RuntimeContext import RuntimeContext


class ModelEditor(QWidget):
    def __init__(self, parent, ctx, model):
        super().__init__(parent)
        self.ctx = ctx
        self.model = model
        self.showModel()

    def showModel(self):
        modelPath = self.me['modelPath']
        with open(modelPath, 'r') as modelData:
            contents = modelData.read()
            editorModel = json.loads(contents)

        # OK, now adopt the model as our 'contents'
        self.me['contents'] = editorModel

    def resizeEvent(self, event):
        size = event.size()
        available = self.ctx.getMEData(self.me, 'drawRect')
        self.ctx.displayManager.layout(available, self.me)

    def paintEvent(self, event):
        self.painter = QPainter()  # Cache for callbacks...rebderers don't need to know
        self.painter.begin(self)

        self.ctx.window.painter = self.painter   # HACK!!
        self.ctx.displayManager.drawModelElement(self.me)

        self.painter.end()


def createPart(ctx, me):
    if 'qtWidget' in me:
        return

    print('create Part: ', me['partType'])

    # Create a tree view
    # widget = ModelEditor(ctx.window, ctx, me)
    # me['qtWidget'] = widget
    modelPath = "../Models/EditorModel.json"
    with open(modelPath, 'r') as modelData:
        appModel = json.load(modelData)
    myCTX = RuntimeContext(appModel, ctx)

    window = myCTX.window
    me['qtWidget'] = window
    window.setParent(ctx.window)
    myCTX.window.show()

def setFocus(ctx, me):
    pass # print('Set Focus:', me['label'])
