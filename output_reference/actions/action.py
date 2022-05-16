from output_reference.elements.element import Element
from output_reference.screenplay import ScreenPlay


class Action (ScreenPlay):
    def __init__(self, name: str):
        super.__init__(self, name)
        self.elements = []

    def interacts_with(self, name: str, element: Element):
        """
        registers some new element to this Action
        :param name: name of the element
        :param element: the object associated to the element
        :return:
        """
        self.elements.append({"name": name, "what": element})
