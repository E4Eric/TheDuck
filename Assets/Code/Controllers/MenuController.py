class MenuController():
    def __init__(self, ctx, menuModel):
        self.ctx = ctx
        self.menuModel = menuModel

        self.highlightME = None

    def highlightElement(self, ctx, me):
        style = me['style']
        if ctx.assetManager.testForStyle(style + " (Over)"):
            me['style'] = me['style'] + " (Over)"
            ctx.window.update()
            self.highlightME = me

    def clearHighlight(self, ctx):
        if self.highlightME != None:
            style = self.highlightME['style']
            style = style.rstrip(' (Over)')
            self.highlightME['style'] = style
            ctx.window.update()
            self.highlightME = None

    def enter(self, ctx, me, x ,y):
        # Hightlight handling...if the style has a ' (Over)' defined switchto it
        self.highlightElement(ctx, me)

    def enter(self, ctx, me, x ,y):
        # Hightlight handling...if the style has a ' (Over)' defined switchto it
        self.highlightElement(ctx, me)

    def leave(self, ctx, me):
        self.clearHighlight(ctx)
