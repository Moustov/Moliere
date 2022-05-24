class ScreenPlay:
    """
    """

    def __init__(self, name: str):
        self.name = name
        self.test_scripts: []

    def is_already_registered(self, name: str, items: [dict]) -> bool:
        """
        Tells if an item name is already in the items list
        :param name:
        :param items: {"name": "XXXX", "what": ScreenPlay}
        :return: True is the name is in items
        """
        for item in items:
            if item["name"] == name:
                return True
        return False

    def play_test_script(self, name: str, scenario: str):
        if not self.is_already_registered(name, scenario):
            self.test_scripts.append(scenario)
        self.play(scenario)

    def run(self, scenario: str):
        print(scenario)
        print("todo: implement this feature")


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

    Act 1 - scene 1 - "a Tester" does "sequence #1"
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
            print(feedback)
        """
