class createController():
    def __init__(self, ctx):
        self.ctx = ctx
        # self.registerHighlightListener()

    def printEvent(self, name, me, x, y):
        type = me['style']
        meStr = f' Type: {type}'
        if 'label' in me:
            meStr += " Label: " + me['label']
        if 'icon' in me:
            meStr += " Icon: " + me['icon']
        if 'tooltp' in me:
            meStr += " Tooltp: " + me['tooltip']
        output = f'Event {name} at ({x}, {y}), ME: {meStr}'
        print(output)


    def enter(self, me, x ,y):
        self.printEvent("Enter", me, x, y)
    def leave(self, me, x, y):
        self.printEvent("Leave", me, x, y)
