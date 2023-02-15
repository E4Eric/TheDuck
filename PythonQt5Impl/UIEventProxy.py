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
        print('enter')

    def leave(self, me):
        print('leave')
        # HACK!! auto remove any tooltip
        self.ctx.displayManager.removeLayer('tooltip')

    def hover(self):
        print('hover')
        if 'hoverAction' in self.curElement:
            action = self.ctx.assetManager.getAction(self.curElement['hoverAction'])
            if action.canExecute(self.ctx, self.curElement):
                action.execute(self.ctx, self.curElement)

    def setCurElement(self, newcurElement):
        if (newcurElement == self.curElement):
            return
        self.leave(self.curElement)
        self.curElement = newcurElement
        self.enter(self.curElement)
        self.printME(self.curElement)

    def mouseMove(self, x, y):
        self.mouseX = x
        self.mouseY = y

        pickedME = self.ctx.displayManager.pick(self.ctx.appModel, x, y)
        self.setCurElement(pickedME)

        def timeout():
            self.hover()
            self.timer = None

        # restart the timer
        if self.timer != None:
            self.timer.cancel()
        self.timer = threading.Timer(0.3, timeout)
        self.timer.start()

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
