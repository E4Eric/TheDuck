import copy
import time

from PyQt5.QtCore import QTimer


class DisplayManager():
    def __init__(self, window):
        self.window = window

    def addLayer(self, name, me):
        self.window.addLayer(name, me)

    def removeLayer(self, name):
        self.window.removeLayer(name)

    def showPartInWidget(self, me, partType, x, y):
        # First, how big do we need to be ?
        self.layoutElement(0, 0, 10000, 10000, me)
        dr = self.window.getMEData(me, 'drawRect')

        # Now create a model Element for the Widget
        widgetPart = { "style": "Part", "partType": partType, "modelElement": me }
        self.layoutElement(x, y, dr.w, dr.h, widgetPart)

    def showMEInWidget(self, me, x, y):
        # First, how big do we need to be ?
        meToShow = me['modelElement']
        self.layoutElement(0, 0, 10000, 10000, meToShow)
        dr = self.window.getMEData(meToShow, 'drawRect')

        # Now create a model Element for the Widget
        self.layoutElement(x, y, dr.w, dr.h, me)

    def getLayoutCode(self, me):
        if 'layout' in me:
            return self.window.assetManager.getLayout(me['layout'])

        sd = self.window.assetManager.getStyleData(me['style'])
        return self.window.assetManager.getLayout(sd['layout'])

    def getRendererCode(self, me):
        if 'layout' in me:
            return self.window.assetManager.getrenderer(me['renderer'])

        sd = self.window.assetManager.getStyleData(me['style'])
        return self.window.assetManager.getRenderer(sd['renderer'])

    def layoutModel(self, available):
        start = time.perf_counter()
        available = self.layout(available, self.window.appModel)
        end = time.perf_counter()
        # print('Layout Model: ', end - start)

    def layoutElement(self, x, y ,w, h, me):
        available = copy.copy(self.window.getMEData(self.window.appModel, 'drawRect'))
        available.x = x
        available.y = y
        available.w = w
        available.h = h
        self.layout(available, me)

    def layout(self, available, me):
        layout = self.getLayoutCode(me)
        available = layout.layout(self.window, available, me)
        return available

    def drawModel(self):
        start = time.perf_counter()
        self.drawModelElement(self.window.appModel)
        end = time.perf_counter()
        # print('Draw: ', end - start)


    def drawModelElement(self, me):
        # auto-draw the frame if the me has a 'style' that's not already frame
        if 'style' in me and me['style'] != 'frame':
            renderer = self.window.assetManager.getRenderer('frame')
            renderer.draw(self.window, me)

        sd = self.window.assetManager.getStyleData(me['style'])
        renderer = self.getRendererCode(me)
        renderer.draw(self.window, me)
        if 'contents' in me:
            for kid in me['contents']:
                self.drawModelElement(kid)

    def refresh(self):
        available = self.window.getMEData(self.window.appModel, 'drawRect')
        self.layoutModel(available)
        self.window.forceUpdate(0, 0, 0, 0)

    def pickElement(self, me, x, y):
        dr = self.window.getMEData(me, 'drawRect')
        if x < dr.x:
            return None
        if x > (dr.x + dr.w):
            return None
        if y < dr.y:
            return None
        if y > (dr.y + dr.h):
            return None

        # drill down
        if 'contents' in me:
            for kid in me['contents']:
                found = self.pickElement(kid, x,y)
                if found != None:
                    return found
        return me

    def pick(self, me, x ,y):
        # now check the display structure
        return self.pickElement(me, x, y)
