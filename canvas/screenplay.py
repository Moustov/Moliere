from moliere_core_domain.moliere_parser import extract_screenplay_objects
from screenplay_specific_domain.skeleton_generator import SkeletonGenerator


class ScreenPlay:
    """
    """

    def __init__(self, name: str):
        self.name = name
        self.test_scripts = []

    def process_moliere_script(self, moliere_script: str) -> str:
        """
        :param moliere_script:
        :return:
        """

        self.transforms_moliere_script_into_scenario(moliere_script)

    def play_test_script(self, name: str, scenario: str) -> str:
        """

        :param moliere_script: something like ```
            Act 1 - scene 1 - "John" does "sequence #1"
                # SCENE SETUP
                    an_actor.name = "John"
                    element_1.can_be_found_on(page_1)
                    element_2.can_be_found_on(page_1)
                    element_3.can_be_found_on(page_2)
                    element_4.can_be_found_on(page_1)
                    element_5.can_be_found_on(the_mailbox)
                    action_1.add_interaction(element_1)
                    action_2.add_interaction(element_3)
                    a_task.set_sequence([{"task": "sequence #1",
                                        "actions": [{"sequence": 1, "action": action_1, "param": 123},
                                                    {"sequence": 2, "action": action_2, "param": click}])
                # SCENE PLAY
                    an_actor.accomplishes(a_task)

            Act 1 - scene 1 - "a Tester" does "sequence of checks #1"
                # SCENE SETUP
                    another_actor.name = "a Tester"
                    action_3.add_interaction(element_4)
                    action_4.add_feedback(element_5)
                    checks_1 = [{"task": "sequence of checks #1",
                                "actions": [{"action": action_3, "sequence": 1, "param": 456},
                                            {"check": action_4, "sequence": 2}]
                # SCENE PLAY
                    a_test.set_actions(checks_1)
                    feedback = another_actor.accomplishes(checks_1)
                    print(feedback) ```
        :return: something like
            "John does the sequence #1
                -> <action_1.name> with 123 on element_1 in page 1
                -> and <action_2.name> with a click on element_3 in page 2
            Then a Tester does the sequence of checks #2
                -> <action_3.name> with 456
                <- and sees 32 EUR from element_5 in the_mailbox"
        """
        spectator_view = """John does the sequence #1
    -> <action_1.name> with 123 on element_1 in page 1
    -> and <action_2.name> with a click on element_3 in page 2
Then a Tester does the sequence of checks #2
    -> <action_3.name> with 456
    <- and sees 32 EUR from element_5 in the_mailbox"""
        return spectator_view

    def perform_action(self, line) -> str:
        """
        process the line and return the outcome of the operation from a spectator's point of view
        :param line:
        :return:
        """
        return line  # implement some code to perform the operation

    def transforms_moliere_script_into_scenario(self, moliere_script) -> str:
        """
        generate
        :param moliere_script:
        :return:
        """
        return None


if __name__ == '__main__':
    test_script = """
    Act 1 - scene 1 - "John" does "sequence #1"
        # SCENE SETUP
            an_actor.name = "John"
            element_1.can_be_found_on(page_1)
            element_2.can_be_found_on(page_1)
            element_3.can_be_found_on(page_2)
            element_4.can_be_found_on(page_1)
            element_5.can_be_found_on(the_mailbox)
            action_1.add_interaction(element_1)
            action_2.add_interaction(element_3)
            a_task.set_sequence([{"task": "sequence #1", 
                                "actions": [{"sequence": 1, "action": action_1, "param": 123}, 
                                            {"sequence": 2, "action": action_2, "param": click}])
        # SCENE PLAY
            an_actor.accomplishes(a_task)

    Act 1 - scene 2 - "a Tester" does "sequence #2"
        # SCENE SETUP
            another_actor.name = "a Tester"
            action_3.add_interaction(element_4)
            action_4.add_feedback(element_5)
            checks_1 = [{"task": "sequence of checks #2", 
                        "actions": [{"action": action_3, "sequence": 1, "param": 456},
                                    {"check": action_4, "sequence": 2}]
        # SCENE PLAY
            a_test.set_actions(checks_1)
            feedback = another_actor.accomplishes(checks_1)
            print(feedback)
        """
    my_comedy = ScreenPlay("Much ado about nothing")
    output = my_comedy.play_test_script("act 1", test_script)
    print(output)
