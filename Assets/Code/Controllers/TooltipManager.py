class createController():
    def __init__(self, ctx):
        self.ctx = ctx
        self.tooltipShowing = False

    def showTooltip(self, me, x, y):
        tooltipME = { 'style': "Tooltip", "label": me['tooltip'] }
        self.ctx.displayManager.layoutElement(x, y, 10000, 1000, tooltipME)
        self.ctx.displayManager.addLayer("Tooltip", tooltipME)
        self.tooltipShowing = True

    def hideTooltip(self):
        if self.tooltipShowing:
            self.ctx.displayManager.removeLayer("Tooltip")
            self.tooltipShowing = False

    def hover(self, me, x, y):
        if 'tooltip'in me:
            self.showTooltip(me, x ,y)

    def leave(self, me, x, y):
        self.hideTooltip()
