from unittest import TestCase
from deepdiff import DeepDiff
from extract_objects import extract_screenplay_objects


class Test(TestCase):
    def test_extract_objects_empty(self):
        my_scene = ""
        expected_screenplay_generated_parts = {
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
        self.assertDictEqual(screen_play_generated_parts, expected_screenplay_generated_parts)

    def test_extract_objects_screenplay_basic(self):
        my_scene = """
                    > GIVEN <Actor> who can <Ability>
                    > WHEN <Actor> does <Task> at <Parameters>
                    > THEN <Actor> checks <Question> is <Assertion>
                    >       THANKS TO <element> FOUND ON <screen>
                    """
        expected_screenplay_generated_parts = {
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
        self.assertDictEqual(screen_play_generated_parts, expected_screenplay_generated_parts)

    def test_extract_objects_screenplay_with_jack(self):
        my_scene = """
        GIVEN <Jack> who can <browse the web> and <call HTTP APIs> and <go to the pub>
        WHEN <Jack> does <go to the pub> at <The Sheep's Head Pub>
            AND <order> with <999 beers>
            THEN <Jack> checks <the total amount> is <999 × 2.59 EUR>
                      THANKS TO <the total amount> FOUND ON <the bill>
        """
        expected_screenplay_generated_parts = {
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
        diff = DeepDiff(screen_play_generated_parts, expected_screenplay_generated_parts, ignore_order=True)
        self.assertEqual(diff, {})

    def test_extract_objects_screenplay_with_jack_and_multiple_checks(self):
        my_scene = """
        GIVEN <Jack> who can <browse the web> and <call HTTP APIs> and <go to the pub>
        WHEN <Jack> does <go to the pub> at <The Sheep's Head Pub>
            AND <order> with <999 beers>
            THEN <Jack> checks
                    <the total amount> is <999 × 2.59 EUR> THANKS TO <the total amount> FOUND ON <the bill>
                    AND <the table number> is <the good one> THANKS TO <the table number> FOUND ON <the bill>
        """
        expected_screen_play_generated_parts = {
            "actors": ["Jack"],
            "facts": [],
            "tasks": ["go to the pub", "order"],
            "questions": [{"check": "the total amount", "is": "999 × 2.59 EUR"},
                          {"check": "the table number", "is": "the good one"}
                          ],
            "elements": [{"item": "The Sheep's Head Pub", "screen": None},
                         {"item": "browse the web", "screen": None},
                         {"item": "call HTTP APIs", "screen": None},
                         {"item": "go to the pub", "screen": None},
                         {"item": "order", "screen": None},
                         {"item": "999 beers", "screen": None},
                         {"item": "the total amount", "screen": "the bill"},
                         {"item": "the table number", "screen": "the bill"}
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