class createController():
    def __init__(self, window):
        self.window = window
        self.curME = None

    def enter(self, window, me, x ,y):
        print("enter")

    def leave(self, window, me):
        print("leave")

    def resizeEvent(self, window, w, h):
        print("editor resized")
