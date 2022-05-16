from canvas.element import Element


class Action:
    def __init__(self):
        self.elements = []

    def add_element(self, name: str, element: Element):
        """
        registers some new element to this Action
        :param name: name of the element
        :param element: the object associated to the element
        :return:
        """
        self.elements.append({"name": name, "what": element})

    def interact_with(self):
        pass
