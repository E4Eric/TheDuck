class MenuController():
    def __init__(self, ctx, menuModel):
        self.ctx = ctx
        self.menuModel = menuModel

        self.highlightME = None

    def highlightElement(self, me):
        style = me['style']
        if self.ctx.assetManager.testForStyle(style + " (Over)"):
            me['style'] = me['style'] + " (Over)"
            self.ctx.window.update()
            self.highlightME = me

    def clearHighlight(self):
        if self.highlightME != None:
            style = self.highlightME['style']
            style = style.rstrip(' (Over)')
            self.highlightME['style'] = style
            self.ctx.window.update()
            self.highlightME = None

    def enter(self, me, x ,y):
        # Hightlight handling...if the style has a ' (Over)' defined switchto it
        self.highlightElement(me)

    def enter(self, me, x ,y):
        # Hightlight handling...if the style has a ' (Over)' defined switchto it
        self.highlightElement(me)

    def leave(self, me, x, y):
        self.clearHighlight()
