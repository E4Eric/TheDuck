import threading

class UIEventProxy():
    def __init__(self, ctx):
        self.ctx = ctx

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

        self.curElement = None
        self.timer = None

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

    def mouseMove(self, x, y):
        pickedME = self.pick(self.ctx.appModel, x, y)
        if pickedME != None:
            if pickedME != self.curElement:
                self.curElement = pickedME
                str = pickedME['style']
                if 'label' in pickedME:
                    str += ' Label: ' + pickedME['label']
                if 'icon' in pickedME:
                    str += ' Label: ' + pickedME['icon']
                print(str)

        def timeout():
            print("Hover !")
            self.timer = None

        # restart the timer
        if self.timer != None:
            self.timer.cancel()
        self.timer = threading.Timer(1, timeout)
        self.timer.start()

        self.mouseX = x
        self.mouseY = y

    def mousePressEvent(self, button):
        print(button, " pressed !")

        self.downX = self.mouseX
        self.downY = self.mouseY

        if button == 'left':
           lButton = True
        if button == 'right':
           rButton = True
        if button == 'Middle':
           mButton = True

    def mouseReleaseEvent(self, button):
        print(button, " released !")

        if button == 'left':
           lButton = False
        if button == 'right':
           rButton = False
        if button == 'Middle':
           mButton = False

        self.downX = 0
        self.downY = 0
