class createController():
    def __init__(self):
        self.tooltipShowing = False

    def showTooltip(self, window, me, x, y):
        tooltipME = { 'style': "Tooltip", "label": me['tooltip'] }
        window.displayManager.layoutElement(x, y, 10000, 1000, tooltipME)
        window.displayManager.addLayer("Tooltip", tooltipME)
        self.tooltipShowing = True

    def hideTooltip(self, window):
            window.displayManager.removeLayer("Tooltip")
            self.tooltipShowing = False

    def hover(self, window, me, x, y):
        if me == None:
            self.hideTooltip(window)
            return

        if 'tooltip'in me:
            self.showTooltip(window, me, x ,y)

    def leave(self, window, me):
        self.hideTooltip(window)

    def enterWidget(self, window, x, y):
        self.hideTooltip(window)

    def leaveWidget(self, window):
        self.hideTooltip(window)
