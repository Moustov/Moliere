from canvas.action import Action
from canvas.actor import Actor


class Task:
    def __init__(self, name: str):
        super.__init__(self, name)
        self.made_of = []

    def made_up_of(self, an_actor: Actor):
        pass
