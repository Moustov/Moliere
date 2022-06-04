from canvas.element import Element
from canvas.task import Task


class Question:
    def __init__(self, name: str, a_task: Task, action_on_an_element: Element, assert_value_from_an_element: Element):
        self.task = a_task
        self.action_to_assert = action_on_an_element
        self.assert_value = assert_value_from_an_element
        self.name = name

    def ask_about_assert_status(self) -> bool:
        """
        should run the question and return its status
        :return:
        """
        print("Implement the question in your Question object")
        return False

    def run(self) -> str:
        """
        should print something like:
        Then a Tester does the sequence of checks #2
            -> <action_3.name> with 456
            <- and sees 32 EUR from element_5 in the_mailbox
        :return:
        """
        res = self.task.run()
        res += f"<- and sees {self.assert_value.get_value()} from {self.assert_value.name} in {self.assert_value.screen}"
        return res
