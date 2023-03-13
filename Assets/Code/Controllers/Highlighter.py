class createController():
    def __init__(self, ctx):
        self.ctx = ctx
        self.highlightME = None
        # self.registerHighlightListener()

    # def registerHighlightListener(self):
    #     def highlightListener(ctx, me, attName, oldVal, newVal):
    #         print(f'highlight Changed: was {oldVal} is {newVal}')
    #         ctx.window.update()
    #
    #     self.ctx.subscribe('highlighter', highlightListener)

    def highlightElement(self, me):
        style = me['style']
        if self.ctx.assetManager.testForStyle(style + " (Over)"):
            me['style'] = me['style'] + " (Over)"
            self.ctx.window.update()
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
        style = me['style']
        if ctx.assetManager.testForStyle(style + " (Over)"):
            self.highlightElement(me)

    def leave(self, ctx, me):
        self.clearHighlight(ctx)

