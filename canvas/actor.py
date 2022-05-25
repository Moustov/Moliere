from canvas.ability import Ability
from canvas.fact import Fact
from canvas.question import Question
from canvas.task import Task


class Actor:
    def __init__(self, name: str):
        super.__init__(self, name)
        self.abilities = []

    def can(self, name: str, ability: Ability):
        """
        registers some new ability to this actor
        :param name: name of the ability
        :param ability: the object associated to the ability
        :return:
        """
        if not self.is_already_registered(name, self.abilities):
            self.abilities.append({"name": name, "what": ability})

    def learns(self, a_fact: Fact):
        pass

    def asks(self, a_question: Question):
        pass

    def does(self, a_task: Task):
        pass
