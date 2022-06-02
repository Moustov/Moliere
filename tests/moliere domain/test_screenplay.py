from unittest import TestCase

from deepdiff import DeepDiff

from canvas.screenplay import ScreenPlay
from moliere_core_domain.scene_setup import Scene


class TestScreenPlay(TestCase):
    def test_add_moliere_script(self):
        a_scene = Scene("output")
        line_1 = """
            GIVEN <Jack Donald> who can <browse the web> and <call HTTP APIs> and <go to the pub>
            WHEN <Jack Donald> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack Donald> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            """
        a_scene.add_moliere_script("act 1 - scene #1 - line #1", line_1)
        line_2 = """
            GIVEN <Jack Donald> who can <play music>
            WHEN <Jack Donald> does <play music> at <The Sheep's Head Pub>
                THEN <Jack Donald> checks <the gig reward> is <500 EUR>
                          THANKS TO <earned money> FOUND ON <the table>
            """
        a_scene.add_moliere_script("act 1 - scene #1 - line #2", line_2)
        expected_screenplay_objects = {
            "actors": ["Jack Donald"],
            "facts": [],
            "tasks": ["go to the pub", "order", "play music"],
            "questions": [{"check": "the total amount", "is": "999 × 2.59 EUR"},
                          {"check": "the gig reward", "is": "500 EUR"}],
            "elements": [{"item": "The Sheep's Head Pub", "screen": None},
                         {"item": "browse the web", "screen": None},
                         {"item": "call HTTP APIs", "screen": None},
                         {"item": "go to the pub", "screen": None},
                         {"item": "order", "screen": None},
                         {"item": "999 beers", "screen": None},
                         {"item": "the total amount", "screen": "the bill"},
                         {"item": "earned money", "screen": "the table"}
                         ],
            "screens": ["the bill", "the table"],
            "abilities": ["browse the web", "call HTTP APIs", "go to the pub", "order", "play music"],
            "actions": [
                {"do": "go to the pub", "direct object": "The Sheep's Head Pub"},
                {"do": "play music", "direct object": "The Sheep's Head Pub"},
                {"do": "order", "direct object": "999 beers"}
            ]
        }
        diff = DeepDiff(a_scene.my_screenplay_objects, expected_screenplay_objects, ignore_order=True)
        self.assertEqual(diff, {})


    def test_generate_test_script(self):
        pass

    def test_play_test_script(self):
        test_script = """        Act 1 - scene 1 - "John" does "sequence #1"
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
        expected_output = """John does the sequence #1
    -> <action_1.name> with 123 on element_1 in page 1
    -> and <action_2.name> with a click on element_3 in page 2
Then a Tester does the sequence of checks #2
    -> <action_3.name> with 456
    <- and sees 32 EUR from element_5 in the_mailbox"""
        my_comedy = ScreenPlay("Much ado about nothing")
        output = my_comedy.play_test_script("act 1", test_script)
        print(output)
        self.assertEqual(output, expected_output)
