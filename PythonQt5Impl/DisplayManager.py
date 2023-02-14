import time

class DisplayManager():
    def __init__(self, ctx):
        self.ctx = ctx
        self.layers = {}

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
        print('Layout Model: ', end - start)

    def layout(self, available, me):
        layout = self.getLayoutCode(me)
        available = layout.layout(self.ctx, available, me)
        return available

    def drawModel(self):
        start = time.perf_counter()
        self.drawModelElement(self.ctx.appModel)
        end = time.perf_counter()
        print('Draw: ', end - start)


    def drawModelElement(self, me):
        if 'drawRect' not in me:
            return   # No-op

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
    def pick(self, me, x ,y):
        if 'drawRect' not in me:
            return None

        dr = me['drawRect']
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
                found = self.pick(kid, x,y)
                if found != None:
                    return found
        return me
