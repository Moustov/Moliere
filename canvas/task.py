from canvas.action import Action
from canvas.actor import Actor
from canvas.element import Element


class Task:
    def __init__(self, sequence_name: str, actor=Actor):
        self.made_of = []
        self.name = sequence_name
        self.actor = actor

    def made_up_of(self, action_on_an_element: Action, value_from_an_element: str):
        self.made_of.append({"what": action_on_an_element, "value": value_from_an_element})

    def run(self) -> str:
        """
        should print something like
        John does the sequence #1
            -> <action_1.name> with 123 on element_1 in page 1
            -> and <action_2.name> with a click on element_3 in page 2
        :return:
        """
        res = f"{self.actor} does the sequence f{self.name} "
        actions = []
        for action in self.made_of:
            actions.append(f"-> {action['what'].name} with {action['value']} in {action['what'].element.screen()}")
        res += " and ".join(actions)
        return res
