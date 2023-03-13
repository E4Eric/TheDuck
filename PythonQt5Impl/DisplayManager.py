import copy
import time

from PyQt5.QtCore import QTimer


class DisplayManager():
    def __init__(self, ctx):
        self.ctx = ctx

    def addLayer(self, name, me):
        print(f' *** App Draw Rect (before addLayer): {self.ctx.getMEData(self.ctx.appModel, "drawRect")}')
        self.ctx.window.addLayer(name, me)
        print(f' *** App Draw Rect (after addLayer): {self.ctx.getMEData(self.ctx.appModel, "drawRect")}')

    def removeLayer(self, name):
        self.ctx.window.removeLayer(name)

    def showPartInWidget(self, me, partType, x, y):
        # First, how big do we need to be ?
        self.layoutElement(0, 0, 10000, 10000, me)
        dr = self.ctx.getMEData(me, 'drawRect')

        # Now create a model Element for the Widget
        widgetPart = { "style": "Part", "partType": partType, "modelElement": me }
        self.layoutElement(x, y, dr.w, dr.h, widgetPart)

    def showMEInWidget(self, me, x, y):
        # First, how big do we need to be ?
        meToShow = me['modelElement']
        self.layoutElement(0, 0, 10000, 10000, meToShow)
        dr = self.ctx.getMEData(meToShow, 'drawRect')

        # Now create a model Element for the Widget
        self.layoutElement(x, y, dr.w, dr.h, me)

    def getLayoutCode(self, me):
        if 'layout' in me:
            return self.ctx.assetManager.getLayout(me['layout'])

        sd = self.ctx.assetManager.getStyleData(me['style'])
        return self.ctx.assetManager.getLayout(sd['layout'])

    def getRendererCode(self, me):
        if 'layout' in me:
            return self.ctx.assetManager.getrenderer(me['renderer'])

        sd = self.ctx.assetManager.getStyleData(me['style'])
        return self.ctx.assetManager.getRenderer(sd['renderer'])

    def layoutModel(self, available):
        start = time.perf_counter()
        available = self.layout(available, self.ctx.appModel)
        end = time.perf_counter()
        # print('Layout Model: ', end - start)

    def layoutElement(self, x, y ,w, h, me):
        available = copy.copy(self.ctx.getMEData(self.ctx.appModel, 'drawRect'))
        available.x = x
        available.y = y
        available.w = w
        available.h = h
        self.layout(available, me)

    def layout(self, available, me):
        layout = self.getLayoutCode(me)
        available = layout.layout(self.ctx, available, me)
        return available

    def drawModel(self):
        start = time.perf_counter()
        self.drawModelElement(self.ctx.appModel)
        end = time.perf_counter()
        # print('Draw: ', end - start)


    def drawModelElement(self, me):
        # auto-draw the frame if the me has a 'style' that's not already frame
        if 'style' in me and me['style'] != 'frame':
            renderer = self.ctx.assetManager.getRenderer('frame')
            renderer.draw(self.ctx, me)

        sd = self.ctx.assetManager.getStyleData(me['style'])
        renderer = self.getRendererCode(me)
        renderer.draw(self.ctx, me)
        if 'contents' in me:
            for kid in me['contents']:
                self.drawModelElement(kid)

    def refresh(self):
        available = self.ctx.getMEData(self.ctx.appModel, 'drawRect')
        self.layoutModel(available)
        self.ctx.window.forceUpdate(0, 0, 0, 0)

    def pickElement(self, me, x, y):
        dr = self.ctx.getMEData(me, 'drawRect')
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
