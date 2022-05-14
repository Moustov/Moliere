from unittest import TestCase

from generate_screenplay import generate_screenplay, extract_keyword_in_delimiter


class Test(TestCase):
    def test_generate_screenplay_empty(self):
        my_scene = ""
        expected_screen_play_generated_parts = {
            "actors": [],
            "facts": [],
            "tasks": [],
            "questions": [],
            "elements": [],
            "screens": [],
            "abilities": [],
            "actions": []
        }
        screen_play_generated_parts = generate_screenplay(my_scene)
        self.assertDictEqual(screen_play_generated_parts, expected_screen_play_generated_parts)

    def test_generate_screenplay_basic(self):
        my_scene = """
                    > GIVEN <Actor> who can <Ability>
                    > WHEN <Actor> does <Task> <Parameters>
                    > THEN <Actor> checks <Question> is <Assertion… on Answer>
                    > THANKS TO <element> FOUND ON <screen>
                    """
        expected_screen_play_generated_parts = {
            "actors": ["Actor"],
            "facts": [],
            "tasks": [],
            "questions": [],
            "elements": [],
            "screens": [],
            "abilities": ["Ability"],
            "actions": [{"do": "Task", "direct object": "Parameters"}]
        }
        screen_play_generated_parts = generate_screenplay(my_scene)
        self.assertDictEqual(screen_play_generated_parts, expected_screen_play_generated_parts)

    # def test_generate_screenplay_with_jack(self):
    #     my_scene = """
    #     GIVEN <Jack> who can <browse the web> and <call HTTP APIs> and <go to the pub>
    #     WHEN <Jack> does <go to the pub> <The Sheep's Head Pub>
    #         AND does <order> <999 beers>
    #         THEN <Jack> checks <the bill's total amount> <is 999 × 2.59 EUR>
    #         THANKS TO <the bill's total amount> FOUND ON <receipt>
    #     """
    #     expected_screen_play_generated_parts = {
    #         "actors": ["Jack"],
    #         "facts": [],
    #         "tasks": ["go to the pub", "order"],
    #         "questions": [{"check": "the bill's total amount", "is": "is 999 × 2.59 EUR"}],
    #         "elements": ["The Sheep's Head Pub", "999 beers", "the bill's total amount"],
    #         "screens": ["receipt"],
    #         "abilities": ["browse the web", "call HTTP APIs", "go to the pub"],
    #         "actions": [
    #             {"do": "go to the pub", "direct object": "The Sheep's Head Pub"},
    #             {"do": "order", "direct object": "999 beers"}
    #         ]
    #     }
    #     screen_play_generated_parts = generate_screenplay(my_scene)
    #     self.assertDictEqual(screen_play_generated_parts, expected_screen_play_generated_parts)

    def test_extract_keyword_in_delimiter(self):
        actor = extract_keyword_in_delimiter("<Actor>")
        self.assertEqual(actor, "Actor")
