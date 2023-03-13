class createController():
    def __init__(self, ctx):
        self.ctx = ctx

        self.highlightME = None
        self.tooltipShowing = False

        self.controllers = []
        self.registerControllers()

    def registerController(self, name):
        module = self.ctx.assetManager.getController(name)
        controller = module.createController(self.ctx)
        self.controllers.append(controller)

    def registerControllers(self):
        self.registerController("Highlighter")
        self.registerController('TooltipManager')


    def enter(self, ctx, me, x ,y):
        for controller in self.controllers:
            if hasattr(controller, 'enter'):
                controller.enter(self.ctx, me, x, y)

    def leave(self, ctx, me):
        for controller in self.controllers:
            if hasattr(controller, 'leave'):
                controller.leave(self.ctx, me)
    def hover(self, ctx, me, x, y):
        for controller in self.controllers:
            if hasattr(controller, 'hover'):
                controller.hover(self.ctx, me, x, y)
