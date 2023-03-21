class createController():
    def __init__(self):
        self.highlightME = None
        # self.registerHighlightListener()

    # def registerHighlightListener(self):
    #     def highlightListener(ctx, me, attName, oldVal, newVal):
    #         print(f'highlight Changed: was {oldVal} is {newVal}')
    #         ctx.window.update()
    #
    #     self.ctx.subscribe('highlighter', highlightListener)

    def highlightElement(self, window, me):
        style = me['style']
        if window.assetManager.testForStyle(style + " (Over)"):
            me['style'] = me['style'] + " (Over)"
            window.update()
            self.highlightME = me

    def clearHighlight(self, window):
        if self.highlightME != None:
            style = self.highlightME['style']
            style = style.rstrip(' (Over)')
            self.highlightME['style'] = style
            window.update()
            self.highlightME = None

    def enter(self, window, me, x ,y):
        # Hightlight handling...if the style has a ' (Over)' defined switchto it
        style = me['style']
        if window.assetManager.testForStyle(style + " (Over)"):
            self.highlightElement(window, me)

    def leave(self, window, me):
        self.clearHighlight(window)

