import copy
import importlib
import json
import os
import sys


class AssetManager():
    def __init__(self, ctx):
        self.ctx = ctx
        self.loadAssets(ctx.appModel['assetDir'])

    def loadModules(self, srcDir, moduleCache):
        sys.path.append(srcDir)
        for subdir, dirs, files in os.walk(srcDir):
            for file in files:
                if (file.endswith('.py')):
                    moduleName = file.rstrip('.py')
                    module = importlib.import_module(moduleName)
                    moduleCache[moduleName] = module
                    print(f'   ...{moduleName}')

    def getJsonData(self, srcDir):
        print(srcDir)

        jsonData = []
        for subdir, dirs, files in os.walk(srcDir):
            for file in files:
                if (file.endswith('json')):
                    jsonPath = os.path.join(subdir, file)
                    with open(jsonPath, 'r') as myfile:
                        jsonString = myfile.read()

                    # parse file and cache the result
                    jsonObj = json.loads(jsonString)
                    jsonData.append(jsonObj)
        return jsonData

    def cacheImage(self, name, image):
        self.imageCache[name] = image

    def loadStyleSheets(self, stylesDir):
        styleSheetList = self.getJsonData(stylesDir)
        for styleSheet in styleSheetList:
            self.styleCache[styleSheet['name']] = styleSheet
            print("Loaded Style: " + styleSheet['name'])
            imagePath = stylesDir + '/' + styleSheet['imagePath']
            image = self.ctx.window.loadImage(imagePath)
            self.cacheImage('Style Sheet/' + styleSheet['name'], image)

    def testForStyle(self, styleName):
        styleSheet = self.styleCache[self.ctx.appModel['curStyleSheet']]
        return styleName in styleSheet['Styles']

    def getStyleData(self, styleName):
        styleSheet = self.styleCache[self.ctx.appModel['curStyleSheet']]
        styleData = styleSheet['Styles'][styleName]
        return styleData

    def getStyleImage(self, styleName):
        cacheName = self.ctx.appModel['curStyleSheet']
        styleSheet = self.styleCache[self.ctx.appModel['curStyleSheet']]
        sheetImage = self.imageCache['Style Sheet/' + styleSheet['name']]
        style = styleSheet['Styles'][styleName]
        styleImage = self.ctx.window.crop(sheetImage, style['srcX'], style['srcY'], style['srcW'], style['srcH'])
        return styleImage

    def getIconImage(self, iconName):
        return self.imageCache['Icon/' + iconName]

    def inflateDrawRectForStyle(self, me):
        styleData = self.getStyleData((me['style']))
        styleExtraW = styleData['lw'] + styleData['lm'] + styleData['rm'] + styleData['rw']
        styleExtraH = styleData['th'] + styleData['tm'] + styleData['bm'] + styleData['bh']
        me['drawRect'].w += styleExtraW
        me['drawRect'].h += styleExtraH

    def adjustAvailableForStyle(self, me, available):
        styleData = self.getStyleData((me['style']))

        adjusted = copy.copy(available)
        adjusted.x += styleData['lw'] + styleData['lm']
        adjusted.y += styleData['th'] + styleData['tm']

        adjusted.w -= styleData['lw'] + styleData['lm'] + styleData['rm'] + styleData['rw']
        adjusted.h -= styleData['th'] + styleData['tm'] + styleData['bm'] + styleData['bh']
        return adjusted

    def loadIconSets(self, iconsDir):
        iconSets = self.getJsonData(iconsDir)

        self.getStyleImage("Transparent Color")
        for iconSet in iconSets:
            imagePath = iconsDir + '/' + iconSet['imagePath']
            iconSrc = self.ctx.window.loadImage(imagePath)

            # HACK!! Allows me to re-use the dark icons (and checks the transparency coce...;-)
            self.ctx.window.setTransparentColor(iconSrc, 81, 86, 88)

            setList = iconSet['iconGrids']
            for iconGrid in setList:
                gridImage = self.ctx.window.crop(iconSrc, iconGrid['srcX'], iconGrid['srcY'], iconGrid['srcW'], iconGrid['srcH'])
                gridX = iconGrid['gridX']
                gridY = iconGrid['gridY']

                # now iterate over the icon name list extracting each icon from the grid
                curX = 0
                for iconName in iconGrid['iconNames']:
                    icon = self.ctx.window.crop(gridImage, curX, 0, gridX, gridY)
                    curX += gridX

                    iconPath = 'Icon/' + iconName
                    self.cacheImage(iconPath, icon)
                    print("loaded Icon: ", iconPath)

    def loadLayouts(self, layoutsDir):
        print(" *** Load Layouts ***")
        self.loadModules(layoutsDir, self.layoutCodeCache)

    def getLayout(self, layoutName):
        return self.layoutCodeCache[layoutName]

    def layout(self, layoutName, available, me):
        code = self.layoutCodeCache[layoutName]
        return code.layout(self.ctx, available, me)

    def loadRenderers(self, renderersDir):
        print(" *** Load Renderers ***")
        self.loadModules(renderersDir, self.rendererCodeCache)

    def getRenderer(self, rendererName):
        return self.rendererCodeCache[rendererName]

    def loadControllers(self, controllersDir):
        print(" *** Load Controllers ***")
        self.loadModules(controllersDir, self.controllerCodeCache)

    def getController(self, controllerName):
        module = self.controllerCodeCache[controllerName]
        return module

    def draw(self, rendererName, me):
        code = self.rendererCodeCache[rendererName]
        code.draw(self.ctx, me)

    def loadActions(self, actionsDir):
        print(" *** Load Actions ***")
        self.loadModules(actionsDir, self.actionCodeCache)

    def getAction(self, actionName):
        return self.actionCodeCache[actionName]

    def doAction(self, actionName, me):
        code = self.actionCodeCache[actionName]
        if code.canExecute(self.ctx, me):
            code.execute(self.ctx, me)

    def loadParts(self, partsDir):
        print(" *** Load Parts ***")
        self.loadModules(partsDir, self.partCodeCache)

    def getPart(self, moduleName):
        return self.partCodeCache[moduleName]

    def layout(self, available, me):
        sd = self.getStyleData((me['style']))
        layoutName = sd['layout']
        layoutCode = self.layoutCodeCache[layoutName]
        available = layoutCode.layout(self.ctx, available, me)
        return available

    def offsetModelElement(self, me, dx, dy):
        me['drawRect'].x += dx
        me['drawRect'].y += dy
        if 'contents' in me:
            for kid in me['contents']:
                self.offsetModelElement(kid, dx, dy)

    def setModelElementPos(self, me, newX, newY):
        dx = newX - me['drawRect'].x
        dy = newY - me['drawRect'].y
        self.offsetModelElement(me, dx, dy)

    def drawModelElement(self, me):
        if 'drawRect' not in me:
            return   # No-op

        # auto-draw the frame if the me has a 'style' that's not already frame
        if 'style' in me and me['style'] != 'frame':
            rendererCode = self.rendererCodeCache['frame']
            rendererCode.draw(self.ctx, me)

        sd = self.getStyleData(me['style'])
        rendererName = sd['renderer']
        rendererCode = self.rendererCodeCache[rendererName]
        rendererCode.draw(self.ctx, me)
        if 'contents' in me:
            for kid in me['contents']:
                self.drawModelElement(kid)

    def loadAssets(self, assetDir):
        # Image-based assets
        self.imageCache = {}  # vgeneric cacne of 'named' images from all other assets

        self.styleCache = {}
        stylesDir = assetDir + "/Images/Styles"
        if os.path.isdir(stylesDir):
            self.loadStyleSheets(stylesDir)

        self.iconCache = {}
        iconsDir = assetDir + "/Images/Icons"
        if os.path.isdir(iconsDir):
            self.loadIconSets(iconsDir)

        # Code-based assets
        self.layoutCodeCache = {}
        layoutsDir = assetDir + "/Code/Layouts"
        if os.path.isdir(layoutsDir):
            self.loadLayouts(layoutsDir)

        self.rendererCodeCache = {}
        rendererssDir = assetDir + "/Code/Renderers"
        if os.path.isdir(rendererssDir):
            self.loadRenderers(rendererssDir)

        self.controllerCodeCache = {}
        controllersDir = assetDir + "/Code/controllers"
        if os.path.isdir(controllersDir):
            self.loadControllers(controllersDir)

        self.actionCodeCache = {}
        actionsDir = assetDir + "/Code/ActionGroups"
        if os.path.isdir(actionsDir):
            self.loadActions(actionsDir)

        self.partCodeCache = {}
        partsDir = assetDir + "/Code/Parts"
        if os.path.isdir(partsDir):
            self.loadParts(partsDir)

