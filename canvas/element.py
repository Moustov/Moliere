from canvas.screen import Screen


class Element:

    def __init__(self, name: str, on_a_screen: Screen = None):
        self.screen = on_a_screen
        self.name = name


    def on_a(self, a_screen: Screen):
        self.screen = a_screen
