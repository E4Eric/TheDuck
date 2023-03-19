class createController():
    def __init__(self, window):
        self.window = window
        self.mainMenuItem = None

    def showMenu(self, me, x, y):
        subMenu = me['submenu']
        menuME = { 'style': "Menu", "contents": subMenu }
        self.window.displayManager.layoutElement(x, y, 10000, 10000, menuME)
        dr = self.window.getMEData(menuME, 'drawRect')
        layerName = f'Menu {me["style"]}  {menuME["id"]}'
        print(f'About to show layer: {layerName}')
        self.window.displayManager.addLayer(layerName, menuME)

    def clearSubMenus(self):
        self.window.clearLayers()
        self.mainMenuItem = None


    def showDropDown(self, me, x, y):
        if self.mainMenuItem != me:
            self.clearSubMenus()

        self.mainMenuItem = me
        dr = self.window.getMEData(me, 'drawRect')
        self.showMenu(me, dr.x, dr.y + dr.h)

    def showSubMenu(self, me, x, y):
        if 'submenu' not in me:
            return

        # Note: when the me is placed in a layer it's moved to (0,0)
        # to align with the widget's top / left...we need to undo this
        # to get the original drawRect
        dr = self.window.getMEData(me, 'drawRect')
        wr = self.window.getPos()
        self.showMenu(me, wr.x + dr.x + wr.w - 2, wr.y + dr.y - 2)

    def enter(self, me, x ,y):
        print(f'Menu Manager: Enter')
        return
        # If the main menu is open and we go over another one then open it
        if self.mainMenuItem != None and 'Main Menu Item' in me['style'] and me != self.mainMenuItem:
            self.showDropDown(me, x, y)

    def lclick(self, me, x, y):
        style = me['style']
        if 'Main Menu Item' in style and 'submenu' in me:
            if me == self.mainMenuItem:
                self.clearSubMenus()
            else:
                self.showDropDown(me, x, y)

        # HACK!! this test is too generic...
        if 'Menu' not in style:
            self.clearSubMenus()

        # Execute meu / toolbar actions
        if 'lclickAction' in me:
            actionModule = self.window.assetManager.getAction(me['lclickAction'])
            if actionModule.canExecute(self.window, me):
                actionModule.execute(self.window, me)

    def hover(self, me, x, y):
        if 'Menu Item' in me['style']:
            if 'Main Menu Item' not in me['style'] and 'submenu' in me:
                self.showSubMenu(me, x, y)
