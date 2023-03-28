

def draw(window, me):
    styleImage = window.assetManager.getStyleImage(me['style'])
    dr = window.getMEData(me, 'drawRect')
    visible = window.crop(styleImage, 0, 0, dr.w, dr.h)
    w = window.getImageWidth(visible)
    h = window.getImageHeight(visible)
    window.drawIcon(200, 200, visible)
    window.drawIcon(dr.x, dr.y, visible)
