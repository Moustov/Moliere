import os
from unittest import TestCase

from skeleton_generator import SkeletonGenerator


class Test(TestCase):
    def test_generate_actors_skeleton_jack(self):
        screenplay_generated_parts = {
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
        output_dir = "output"
        generator = SkeletonGenerator(output_dir)
        generator.generate_skeleton_part(screenplay_generated_parts["actors"], "Actor", True)
        self.assertTrue(os.path.isfile(os.path.normcase(f"{output_dir}/actors/actor.py")))

    def test_generate_actors_skeleton_jack2(self):
        screenplay_generated_parts = {
            "actors": ["Jack Donald"],
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
        output_dir = "output"
        generator = SkeletonGenerator(output_dir)
        generator.generate_skeleton_part(screenplay_generated_parts["actors"], "Actor", True)
        self.assertTrue(os.path.isfile(os.path.normcase(f"{output_dir}/actors/actor.py")))

    def test_refactor_packages_action_simple(self):
        generator = SkeletonGenerator("output", regenerate_project=True)
        imports = """
from canvas.action import Action
"""
        expected_imports = """
from output.actions.action import Action
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

#     def test_refactor_packages_action_all_imports(self):
#         generator = SkeletonGenerator("output")
#         imports = """
# from canvas.action import Action
# from canvas.screenplay import ScreenPlay
# """
#         expected_imports = """
# from output.actions.action import Action
# from output.screenplay import ScreenPlay
# """
#         refactored_imports = generator.refactor_packages(imports)
#         self.assertEqual(refactored_imports, expected_imports)
