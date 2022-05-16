from output_reference.actions.action import Action
from output_reference.actors.actor import Actor
from output_reference.screenplay import ScreenPlay


class Task (ScreenPlay):
    def __init__(self, name: str):
        super.__init__(self, name)
        self.made_of = []

    def made_up_of(self, an_actor: Actor):
        pass
