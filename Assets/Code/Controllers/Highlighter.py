class createController():
    def __init__(self, wndow):
        self.window = wndow
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
        if self.window.assetManager.testForStyle(style + " (Over)"):
            me['style'] = me['style'] + " (Over)"
            self.window.update()
            self.highlightME = me

    def clearHighlight(self):
        if self.highlightME != None:
            style = self.highlightME['style']
            style = style.rstrip(' (Over)')
            self.highlightME['style'] = style
            self.window.update()
            self.highlightME = None

    def enter(self, me, x ,y):
        # Hightlight handling...if the style has a ' (Over)' defined switchto it
        style = me['style']
        if self.window.assetManager.testForStyle(style + " (Over)"):
            self.highlightElement(me)

    def leave(self, me, x, y):
        self.clearHighlight()

