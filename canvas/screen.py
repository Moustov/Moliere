from canvas.element import Element
from canvas.screenplay import ScreenPlay


class Screen (ScreenPlay):
    def __init__(self, name: str):
        super.__init__(self, name)
        self.elements_on_the_screen = []

    def add_element(self, name: str, element: Element):
        """
        registers some new ability to this actor
        :param name: name of the ability
        :param action: the object associated to the ability
        :return:
        """
        self.elements_on_the_screen.append({"name": name, "what": element})