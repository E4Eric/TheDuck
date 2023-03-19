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
        controller = module.createController(self.window)
        self.controllers.append(controller)

    def setControllers(self, names):
        self.controllers = []
        for name in names:
            self.addController(name)

    def enter(self, me):
        if me == None: return

        for controller in self.controllers:
            if hasattr(controller, 'enter'):
                controller.enter(me, self.mouseX, self.mouseY)

    def leave(self, me, x, y):
        if me == None: return

        for controller in self.controllers:
            if hasattr(controller, 'leave'):
                controller.leave(me, x, y)

    def hover(self):
        self.timer.stop()

        for controller in self.controllers:
            if hasattr(controller, 'hover'):
                controller.hover(self.curElement, self.mouseX, self.mouseY)

    def setCurElement(self, newcurElement):
        if (newcurElement == self.curElement):
            return
        self.leave(self.curElement, self.mouseX, self.mouseY)
        self.curElement = newcurElement
        self.enter(self.curElement)


    def mouseMove(self, x, y):
        # print(f'Proxy Mouse Move {x}, {y})')
        self.mouseX = x
        self.mouseY = y

        pickedME = self.window.displayManager.pick(self.window.appModel, x, y)
        self.setCurElement(pickedME)

        # reset the hover timer
        self.timer.start()

        # Drag Support
        for controller in self.controllers:
            if hasattr(controller, 'getDragType'):
                self.dragType = controller.getDragType(self.curElement, x, y)
                if self.dragType != None:
                    self.dragElement = self.curElement
                    self.window.setPointer(self.dragType)
                else:
                    self.dragElement = None
                    self.window.setPointer(self.dragType)

        if self.dragType != None and self.lButton:
            if self.dragType == "EW":  # drag Horizontal
                dx = self.mouseX - self.downX
                if abs(dx) > self.hysteresisSize:
                    for controller in self.controllers:
                        if hasattr(controller, 'dragStart'):
                            controller.dragStart(self.dragElement, x, y)

        # check if we need to test for dragging
        for controller in self.controllers:
            if hasattr(controller, 'dragMove'):
                controller.dragMove(self.dragElement, x, y)

        for controller in self.controllers:
            if hasattr(controller, 'mouseMove'):
                controller.mouseMove(self.curElement, x, y)

    def lclick(self):
       for controller in self.controllers:
            if hasattr(controller, 'lclick'):
                controller.lclick(self.curElement, self.mouseX, self.mouseY)

    def rclick(self):
        for controller in self.controllers:
            if hasattr(controller, 'rclick'):
                controller.rclick(self.curElement, self.mouseX, self.mouseY)

    def mousePressEvent(self, button):
        self.downX = self.mouseX
        self.downY = self.mouseY

        self.lButton = button == 'left'
        if button == 'left':
            self.lButton = True
            self.lclick()
        if button == 'right':
            self.rButton = True
            self.rclick()
        if button == 'middle':
            self.mButton = True

        for controller in self.controllers:
            if hasattr(controller, 'mouseButtonPressed'):
                controller.mouseButtonPressed(button, self.mouseX, self.mouseY)

    def mouseReleaseEvent(self, button):
        self.downX = None
        self.downY = None

        if button == 'left':
           self.lButton = False
        if button == 'right':
           self.rButton = False
        if button == 'middle':
           self.mButton = False

    def enterWidget(self, x, y):
        print('Enter Widget')

    def leaveWidget(self, x, y):
        print('Leave Widget')

