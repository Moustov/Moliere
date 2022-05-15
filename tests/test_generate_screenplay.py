from unittest import TestCase
from deepdiff import DeepDiff
from extract_objects import extract_screenplay_objects


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
        screen_play_generated_parts = extract_screenplay_objects(my_scene)
        self.assertDictEqual(screen_play_generated_parts, expected_screen_play_generated_parts)

    def test_generate_screenplay_basic(self):
        my_scene = """
                    > GIVEN <Actor> who can <Ability>
                    > WHEN <Actor> does <Task> at <Parameters>
                    > THEN <Actor> checks <Question> is <Assertion>
                    >       THANKS TO <element> FOUND ON <screen>
                    """
        expected_screen_play_generated_parts = {
            "actors": ["Actor"],
            "facts": [],
            "tasks": ["Task"],
            "questions": [{"check": "Question", "is": "Assertion"}],
            "elements": [
                {"item": "Ability", "screen": None},
                {"item": "Task", "screen": None},
                {"item": "Parameters", "screen": None},
                {"item": "element", "screen": "screen"}
            ],
            "screens": ["screen"],
            "abilities": ["Ability", "Task"],
            "actions": [{"do": "Task", "direct object": "Parameters"}]
        }
        screen_play_generated_parts = extract_screenplay_objects(my_scene)
        self.assertDictEqual(screen_play_generated_parts, expected_screen_play_generated_parts)

    def test_generate_screenplay_with_jack(self):
        my_scene = """
        GIVEN <Jack> who can <browse the web> and <call HTTP APIs> and <go to the pub>
        WHEN <Jack> does <go to the pub> at <The Sheep's Head Pub>
            AND <order> with <999 beers>
            THEN <Jack> checks <the total amount> is <999 × 2.59 EUR>
                      THANKS TO <the total amount> FOUND ON <the bill>
        """
        expected_screen_play_generated_parts = {
            "actors": ["Jack"],
            "facts": [],
            "tasks": ["go to the pub", "order"],
            "questions": [{"check": "the total amount", "is": "999 × 2.59 EUR"}],
            "elements": [{"item": "The Sheep's Head Pub", "screen": None},
                         {"item": "browse the web", "screen": None},
                         {"item": "call HTTP APIs", "screen": None},
                         {"item": "go to the pub", "screen": None},
                         {"item": "order", "screen": None},
                         {"item": "999 beers", "screen": None},
                         {"item": "the total amount", "screen": "the bill"}
                         ],
            "screens": ["the bill"],
            "abilities": ["browse the web", "call HTTP APIs", "go to the pub", "order"],
            "actions": [
                {"do": "go to the pub", "direct object": "The Sheep's Head Pub"},
                {"do": "order", "direct object": "999 beers"}
            ]
        }
        screen_play_generated_parts = extract_screenplay_objects(my_scene)
        diff = DeepDiff(screen_play_generated_parts, expected_screen_play_generated_parts, ignore_order=True)
        self.assertEqual(diff, {})
