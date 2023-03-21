import threading

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel


class UIEventProxy():
    def __init__(self, window):
        self.window = window

        # Key States
        self.ctrl = False
        self.alt = False
        self.shift = False

        # Mouse
        self.mouseWindow = None
        self.mouseX = 0
        self.mouseY = 0
        self.downX = 0
        self.downY = 0
        self.lButton = False
        self.rButton = False
        self.mButton = False

        # Element handling
        self.curElement = None
        self.dragElement = None

        # Drag Support
        self.dragType = None

        # Initialize the hover timer
        self.timer = QTimer(self.window)
        self.timer.setInterval(500)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hover)

        self.controllers = []

    def addController(self, name):
        module = self.window.assetManager.getController(name)
        controller = module.createController()
        self.controllers.append(controller)

    def setControllers(self, names):
        self.controllers = []
        for name in names:
            self.addController(name)

    def enter(self, window, me, x, y):
        if me == None: return

        for controller in self.controllers:
            if hasattr(controller, 'enter'):
                controller.enter(window, me, self.mouseX, self.mouseY)

    def leave(self, window, me):
        if me == None: return

        for controller in self.controllers:
            if hasattr(controller, 'leave'):
                controller.leave(window, me)

    def hover(self):
        self.timer.stop()

        for controller in self.controllers:
            if hasattr(controller, 'hover'):
                controller.hover(self.mouseWindow, self.curElement, self.mouseX, self.mouseY)

    def setCurElement(self, window, newcurElement):
        if (newcurElement == self.curElement):
            return
        self.leave(window, self.curElement)
        self.curElement = newcurElement
        self.enter(window, self.curElement, self.mouseX, self.mouseY)


    def mouseMove(self, window, x, y):
        # print(f'Proxy Mouse Move {x}, {y})')
        self.mouseWindow = window
        self.mouseX = x
        self.mouseY = y

        pickedME = self.window.displayManager.pick(window.appModel, x, y)
        self.setCurElement(window, pickedME)

        # reset the hover timer
        self.timer.start()

        for controller in self.controllers:
            if hasattr(controller, 'mouseMove'):
                controller.mouseMove(window, self.curElement, x, y)

    def lclick(self, window, me, x, y):
       for controller in self.controllers:
            if hasattr(controller, 'lclick'):
                controller.lclick(window, me, x, y)

    def rclick(self, window, me, x, y):
       for controller in self.controllers:
            if hasattr(controller, 'rclick'):
                controller.rclick(window, me, x, y)

    def mousePressEvent(self, window, button):
        self.downX = self.mouseX
        self.downY = self.mouseY

        self.lButton = button == 'left'
        if button == 'left':
            self.lButton = True
            self.lclick(window, self.curElement, self.mouseX, self.mouseY)
        if button == 'right':
            self.rButton = True
            self.lclick(window, self.curElement, self.mouseX, self.mouseY)
        if button == 'middle':
            self.mButton = True

        for controller in self.controllers:
            if hasattr(controller, 'mouseButtonPressed'):
                controller.mouseButtonPressed(window, button, self.curElement, self.mouseX, self.mouseY)

    def mouseReleaseEvent(self, window, button):
        self.downX = None
        self.downY = None

        if button == 'left':
           self.lButton = False
        if button == 'right':
           self.rButton = False
        if button == 'middle':
           self.mButton = False

        for controller in self.controllers:
            if hasattr(controller, 'mouseButtonReleased'):
                controller.mouseButtonReleased(window, button, self.curElement, self.mouseX, self.mouseY)

    def enterWidget(self, window, x, y):
        for controller in self.controllers:
            if hasattr(controller, 'enterWidget'):
                controller.enterWidget(window, x, y)

    def leaveWidget(self, window):
        for controller in self.controllers:
            if hasattr(controller, 'leaveWidget'):
                controller.leaveWidget(window)

