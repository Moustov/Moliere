from canvas.action import Action
from canvas.actor import Actor
from canvas.element import Element


class Task:
    def __init__(self, name: str):
        self.made_of = []

    def made_up_of(self, an_actor: Actor, an_element: Element, a_param: str):
        self.made_of.append({"actor": an_actor, "what": an_element, "value": a_param})
