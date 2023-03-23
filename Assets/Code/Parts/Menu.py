from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

class MenuFrame(QWidget):
    def __init__(self, ctx, me, parent):
        super().__init__(parent)

        self.ctx = ctx
        self.me = me
        self.parent = parent

    def resizeEvent(self, event):
        size = event.size()
        self.ctx.displayManager.layoutElement(0, 0, size.width(), size.height(), self.me)

    def paintEvent(self, event):
        self.ctx.painter = QPainter()  # Cache for callbacks...rebderers don't need to know
        self.ctx.painter.begin(self)

        self.ctx.displayManager.drawModelElement(self.me)

        self.ctx.painter.end()
        self.ctx.painter = None


def createPart(window, me):
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is not None:
        return

    print('create Part: ', me['partType'])

    # Create the QProgressBar widget and set its orientation to vertical
    menuME = me['modelElement']
    menuFrame = MenuFrame(window, menuME, window)
    menuRect = window.getMEData(menuME, 'drawRect')
    # Display the Menu
    window.setMEData(me, 'qtWidget', menuFrame)

    menuFrame.show()

def setFocus(ctx, me):
    print('Set Focus:', me['label'])
