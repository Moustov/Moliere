import os
from unittest import TestCase

from screenplay_specific_domain.skeleton_generator import SkeletonGenerator


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
        new_class = generator.generate_skeleton_parts_from_items("actors", "Actor",
                                                                 screenplay_generated_parts["actors"], True)
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
        output_dir = "../output"
        generator = SkeletonGenerator(output_dir)
        generator.generate_skeleton_parts_from_items("actors", "Actor", screenplay_generated_parts["actors"], True)
        self.assertTrue(os.path.isfile(os.path.normcase(f"{output_dir}/actors/actor.py")))

    def test_refactor_packages_abilities_simple(self):
        generator = SkeletonGenerator("output", regenerate_project=True)
        imports = """
from canvas.ability import Ability
"""
        expected_imports = """
from output.abilities.ability import Ability
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_actor_simple(self):
        generator = SkeletonGenerator("output", regenerate_project=True)
        imports = """
from canvas.actor import Actor
"""
        expected_imports = """
from output.actors.actor import Actor
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_element_simple(self):
        generator = SkeletonGenerator("output", regenerate_project=True)
        imports = """
from canvas.element import Element
"""
        expected_imports = """
from output.elements.element import Element
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_fact_simple(self):
        generator = SkeletonGenerator("output", regenerate_project=True)
        imports = """
from canvas.fact import Fact
"""
        expected_imports = """
from output.facts.fact import Fact
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_question_simple(self):
        generator = SkeletonGenerator("output", regenerate_project=True)
        imports = """
from canvas.question import Question
"""
        expected_imports = """
from output.questions.question import Question
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_screen_simple(self):
        generator = SkeletonGenerator("output", regenerate_project=True)
        imports = """
from canvas.screen import Screen
"""
        expected_imports = """
from output.screens.screen import Screen
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_task_simple(self):
        generator = SkeletonGenerator("output", regenerate_project=True)
        imports = """
from canvas.task import Task
"""
        expected_imports = """
from output.tasks.task import Task
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_screenplay_simple(self):
        generator = SkeletonGenerator("output", regenerate_project=True)
        imports = """
from canvas.screenplay import ScreenPlay
"""
        expected_imports = """
from output.screenplay import ScreenPlay
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_action_all_imports(self):
        generator = SkeletonGenerator("output")
        imports = """
from canvas.action import Action
from canvas.screenplay import ScreenPlay
"""
        expected_imports = """
from output.actions.action import Action
from output.screenplay import ScreenPlay
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_package_name(self):
        generator = SkeletonGenerator("output")
        package_name = generator.screenplay_classes["actor"].the_class["package"]
        self.assertEqual(package_name, "output.actors")
