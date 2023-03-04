import threading

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

        # Drag parameters
        self.hysteresisSize = 3   # how far the mouse has to move before doing a 'dragStart'

        # Element handling
        self.curElement = None
        self.dragElement = None

        # hover timer
        self.timer = None
        self.timeout = 0.3

        # Drag Support
        self.dragType = None

    def setController(self, controller):
        curController = self.controller
        self.controller = controller
        return curController

    def printME(self, me):
        if me == None:
            print('None')
            return

        str = ""
        if 'label' in me:
            label = me['label']
            str += f'Label: {label} '
        if 'icon' in me:
            label = me['icon']
            str += f'Icon: {label} '
        if 'tooltip' in me:
            label = me['tooltip']
            str += f'Tooltip: {label} '
        print(str)

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
        if (self.curElement != None):
            if self.controller != None:
                if hasattr(self.controller, 'hover'):
                    self.controller.hover(self.ctx, self.curElement)

    def setCurElement(self, newcurElement):
        if (newcurElement == self.curElement):
            return
        self.leave(self.curElement)
        self.curElement = newcurElement
        self.enter(self.curElement)

    def mouseMove(self, x, y):
        self.mouseX = x
        self.mouseY = y

        pickedME = self.ctx.displayManager.pick(self.ctx.appModel, x, y)
        if pickedME == None:
            print("Nothing picked")
        self.setCurElement(pickedME)

        def timeout():
            self.hover()
            self.timer = None

        # restart the timer
        if self.timer != None:
            self.timer.cancel()
        self.timer = threading.Timer(0.3, timeout)
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
        print(button, " pressed !")

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
        print(button, " released !")
        self.downX = None
        self.downY = None

        if button == 'left':
           self.lButton = False
        if button == 'right':
           self.rButton = False
        if button == 'middle':
           self.mButton = False

        self.downX = 0
        self.downY = 0

        if self.controller != None:
            if hasattr(self.controller, 'mouseButtonReleased'):
                self.controller.mouseButtonReleased(self.ctx, button, self.mouseX, self.mouseY)

        if self.dragElement:
            if self.controller != None and self.dragElement != None:
                if hasattr(self.controller, 'dragEnd'):
                    self.controller.dragEnd(self.ctx, self.curElement, self.mouseX, self.mouseY)

