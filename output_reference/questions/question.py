from output_reference.elements.element import Element
from output_reference.screenplay import ScreenPlay


class Question (ScreenPlay):
    def __init__(self, name: str):
        super.__init__(self, name)
        pass

    def about_the_state_of(self, an_element: Element):
        pass
