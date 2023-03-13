import threading

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel


class UIEventProxy():
    def __init__(self, ctx, controller):
        self.ctx = ctx
        self.controller = controller

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
        self.timer = QTimer(self.ctx.window)
        self.timer.setInterval(500)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hover)

    def setController(self, controller):
        curController = self.controller
        self.controller = controller
        return curController

    def enter(self, me):
        if me != None:
            if self.controller != None:
                if hasattr(self.controller, 'enter'):
                    self.controller.enter(self.ctx, me, self.mouseX, self.mouseY)

    def leave(self, me):
        if me != None:
            if self.controller != None:
                if hasattr(self.controller, 'leave'):
                    self.controller.leave(self.ctx, me)

    def hover(self):
        self.timer.stop()
        if (self.curElement != None):
            if self.controller != None:
                if hasattr(self.controller, 'hover'):
                    self.controller.hover(self.ctx, self.curElement, self.mouseX, self.mouseY)

    def setCurElement(self, newcurElement):
        if (newcurElement == self.curElement):
            return
        self.leave(self.curElement)
        self.curElement = newcurElement
        self.enter(self.curElement)


    def mouseMove(self, x, y):
        # print(f'Proxy Mouse Move {x}, {y})')
        self.mouseX = x
        self.mouseY = y

        # print(f' *** App Draw Rect: {self.ctx.getMEData(self.ctx.appModel, "drawRect")}')
        pickedME = self.ctx.displayManager.pick(self.ctx.appModel, x, y)
        self.setCurElement(pickedME)

        # reset the hover timer
        self.timer.start()

        # Drag Support
        if self.controller != None:
            if hasattr(self.controller, 'getDragType'):
                self.dragType = self.controller.getDragType(self.ctx, self.curElement, x, y)
                if self.dragType != None:
                    self.dragElement = self.curElement
                    self.ctx.window.setPointer(self.dragType)
                else:
                    self.dragElement = None
                    self.ctx.window.setPointer(self.dragType)

        if self.dragType != None and self.lButton:
            if self.dragType == "EW":  # drag Horizontal
                dx = self.mouseX - self.downX
                if abs(dx) > self.hysteresisSize:
                    if self.controller != None:
                        if hasattr(self.controller, 'dragStart'):
                            self.controller.dragStart(self.ctx, self.dragElement, x, y)

        # check if we need to test for dragging
        if self.dragElement != None:
            if hasattr(self.controller, 'dragMove'):
                self.controller.dragMove(self.ctx, self.dragElement, x, y)

        if self.controller != None:
            if hasattr(self.controller, 'mouseMove'):
                self.controller.mouseMove(self.ctx, self.curElement, x, y)

    def lclick(self):
        if self.controller != None:
            if hasattr(self.controller, 'lclick'):
                self.controller.lclick(self.ctx, self.curElement, self.mouseX, self.mouseY)

    def rclick(self):
        if self.controller != None:
            if hasattr(self.controller, 'rclick'):
                self.controller.rclick(self.ctx, self.curElement, self.mouseX, self.mouseY)

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

        if self.controller != None:
            if hasattr(self.controller, 'mouseButtonPressed'):
                self.controller.mouseButtonPressed(self.ctx, button, self.mouseX, self.mouseY)

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

