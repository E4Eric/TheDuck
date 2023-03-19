class createController():
    def __init__(self, ctx):
        self.ctx = ctx

        self.controllers = []
        self.registerControllers()

    def registerController(self, name):
        module = self.ctx.assetManager.getController(name)
        controller = module.createController(self.ctx)
        self.controllers.append(controller)

    def registerControllers(self):
        self.registerController("EventTracker")
        self.registerController("Highlighter")
        self.registerController('TooltipManager')
        self.registerController('MenuManager')


    def enter(self, me, x ,y):
        for controller in self.controllers:
            if hasattr(controller, 'enter'):
                controller.enter(me, x, y)

    def leave(self, me, x, y):
        for controller in self.controllers:
            if hasattr(controller, 'leave'):
                controller.leave(me, x, y)
    def hover(self, me, x, y):
        for controller in self.controllers:
            if hasattr(controller, 'hover'):
                controller.hover(me, x, y)
    def lclick(self, me, x, y):
        for controller in self.controllers:
            if hasattr(controller, 'lclick'):
                controller.lclick(me, x, y)
