class createController():
    def __init__(self):
        self.mainMenuItem = None
        self.layerName = None

    def showMenu(self, window, me, x, y):
        subMenu = me['submenu']
        menuME = { 'style': "Menu", "contents": subMenu }
        window.displayManager.layoutElement(x, y, 10000, 10000, menuME)
        dr = window.getMEData(menuME, 'drawRect')
        layerName = f'Menu {me["style"]}  {menuME["id"]}'
        window.displayManager.addLayer(layerName, menuME)

    def clearSubMenus(self, window):
        if self.mainMenuItem is None:
            return

        self.mainMenuItem['style'] = "Main Menu Item"
        self.mainMenuItem = None
        window.clearLayers()


    def showDropDown(self, window, me, x, y):
        # Not all main menu items have submenus (allows 'buttons' on the main menu)
        if 'submenu' not in me:
            return

        if self.mainMenuItem != me:
            self.clearSubMenus(window)

        self.mainMenuItem = me
        self.mainMenuItem['style'] = "Main Menu Item (Open)"
        dr = window.getMEData(me, 'drawRect')
        self.showMenu(window, me, dr.x, dr.y + dr.h)

    def showSubMenu(self, window, me, x, y):
        if 'submenu' not in me:
            return

        # Note: when the me is placed in a layer it's moved to (0,0)
        # to align with the widget's top / left...we need to undo this
        # to get the original drawRect
        dr = window.getMEData(me, 'drawRect')
        wr = window.getPos()
        self.showMenu(window, me, wr.x + dr.x + wr.w - 2, wr.y + dr.y - 2)

    def enter(self, window, me, x ,y):
        # If the main menu is open and we go over another one then open it
        if self.mainMenuItem != None and 'Main Menu Item' in me['style'] and me != self.mainMenuItem:
            self.showDropDown(window, me, x, y)

    def lclick(self, window, me, x, y):
        style = me['style']
        if 'Main Menu Item' in style and 'submenu' in me:
            if me == self.mainMenuItem:
                self.clearSubMenus(window)
            else:
                self.showDropDown(window, me, x, y)

        # HACK!! this test is too generic...
        if 'Menu' not in style:
            self.clearSubMenus(window)

        # Execute meu / toolbar actions
        if 'lclickAction' in me:
            actionModule = window.assetManager.getAction(me['lclickAction'])
            if actionModule.canExecute(window, me):
                actionModule.execute(window, me)

    def hover(self, window, me, x, y):
        if me is None:
            return

        if 'Menu Item' in me['style']:
            if 'Main Menu Item' not in me['style'] and 'submenu' in me:
                self.showSubMenu(window, me, x, y)
