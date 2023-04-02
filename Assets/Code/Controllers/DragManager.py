import json


class createController():
    def __init__(self, window):
        self.window = window

        self.panel = None
        self.sd = None
        self.panelSide = None

        self.okToDrag = False
        self.dragging = False

        self.downX = None
        self.downY = None
        self.trackX = None
        self.trackY = None


    def reset(self, window):
        self.panel = None
        self.sd = None
        self.panelSide = None

        self.okToDrag = False
        self.dragging = False

        self.downX = None
        self.downY = None
        self.trackX = None
        self.trackY = None

        window.setPointer("Default")

    def setDragState(self, window, x, y):
        dr = window.getMEData(self.panel, 'drawRect')
        sd = window.assetManager.getStyleData(self.panel['style'])

        dragWidth = self.panel['dragWidth']
        if self.panelSide == 'left':
            maxX = dr.x + dr.w
            if (maxX - dragWidth) < x <= maxX:
                self.okToDrag = True
                window.setPointer("EW")
            else:
                window.setPointer("Default")

        if self.panelSide == 'bottom':
            if dr.y <= y <= (dr.y + dragWidth):
                self.okToDrag = True
                window.setPointer("NS")
            else:
                window.setPointer("Default")

        if self.panelSide == 'right':
            if dr.x <= x <= (dr.x + dragWidth):
                self.okToDrag = True
                window.setPointer("EW")
            else:
                window.setPointer("Default")

        if self.panelSide == 'top':
            maxY = dr.y + dr.h
            if (maxY - dragWidth) <= y <= maxY:
                self.okToDrag = True
                window.setPointer("NS")
            else:
                window.setPointer("Default")

    def enter(self, window, me, x, y):
        if "dragWidth" in me:
            self.panel = me
            self.sd = window.assetManager.getStyleData(self.panel['style'])
            self.panelSide = self.panel['side']

            self.setDragState(window, x, y)
        # elif self.panel != None:
        #     self.reset(window)

    def leave(self, window, me):
        if not self.dragging:
            self.reset(window)

    def dragStart(self, window, x, y):
        self.dragging = True
        window.grabMouse()

        self.trackX = x
        self.trackY = y

        self.dragMove(window, x, y)

    def dragMove(self, window, x, y):
        panelRect = window.getMEData(self.panel, 'drawRect')

        boundingRect = window.getMEData(window.appModel, 'drawRect')
        if (boundingRect.x + boundingRect.w) - x < 10:
            x = (boundingRect.x + boundingRect.w) -10
        if y - boundingRect.y < 10:
            y = 10
        if (boundingRect.y + boundingRect.h) - y < 10:
            y = (boundingRect.y + boundingRect.h) - 10

        size = 0
        if self.panelSide == 'left':
            size = x - panelRect.x + 5
        elif self.panelSide == 'bottom':
            size = (panelRect.y + panelRect.h) - y + 5
        elif self.panelSide == 'right':
            size = (panelRect.x + panelRect.w) - x
        elif self.panelSide == 'top':
            size = y - panelRect.y

        if size < 10:
            size = 10
        self.panel['size'] = size

        window.displayManager.refresh()

        self.trackX = x
        self.trackY = y

    def mouseMove(self, window, me, x, y):
        if self.panel == None:
            return

        if self.dragging:
            self.dragMove(window, x, y)
        else:
            self.setDragState(window, x, y)

    def lclick(self, window, me, x, y):
        if self.okToDrag:
            self.dragStart(window, x, y)
            self.downX = x
            self.downY = y

    def dragEnd(self, window, me, x, y):
        window.releaseMouse()
        self.dragging = False
        self.reset(window)

    def mouseButtonReleased(self, window, button, me, x, y):
        if self.dragging and button == 'left':
            self.dragEnd(window, me, x, y)


