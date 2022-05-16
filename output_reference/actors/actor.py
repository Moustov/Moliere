from output_reference.abilities.ability import Ability
from output_reference.facts.fact import Fact
from output_reference.questions.question import Question
from output_reference.screenplay import ScreenPlay
from output_reference.tasks.task import Task


class Actor (ScreenPlay):
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
