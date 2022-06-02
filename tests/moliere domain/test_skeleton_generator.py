import os
from unittest import TestCase

from deepdiff import DeepDiff

from moliere_core_domain.scene_setup import Scene
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
        output_dir = "../technical domain/output"
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
        generator = SkeletonGenerator("../technical domain/output", regenerate_project=True)
        imports = """
from canvas.ability import Ability
"""
        expected_imports = """
from output.abilities.ability import Ability
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_actor_simple(self):
        generator = SkeletonGenerator("../technical domain/output", regenerate_project=True)
        imports = """
from canvas.actor import Actor
"""
        expected_imports = """
from output.actors.actor import Actor
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_element_simple(self):
        generator = SkeletonGenerator("../technical domain/output", regenerate_project=True)
        imports = """
from canvas.element import Element
"""
        expected_imports = """
from output.elements.element import Element
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_fact_simple(self):
        generator = SkeletonGenerator("../technical domain/output", regenerate_project=True)
        imports = """
from canvas.fact import Fact
"""
        expected_imports = """
from output.facts.fact import Fact
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_question_simple(self):
        generator = SkeletonGenerator("../technical domain/output", regenerate_project=True)
        imports = """
from canvas.question import Question
"""
        expected_imports = """
from output.questions.question import Question
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_screen_simple(self):
        generator = SkeletonGenerator("../technical domain/output", regenerate_project=True)
        imports = """
from canvas.screen import Screen
"""
        expected_imports = """
from output.screens.screen import Screen
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_task_simple(self):
        generator = SkeletonGenerator("../technical domain/output", regenerate_project=True)
        imports = """
from canvas.task import Task
"""
        expected_imports = """
from output.tasks.task import Task
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_screenplay_simple(self):
        generator = SkeletonGenerator("../technical domain/output", regenerate_project=True)
        imports = """
from canvas.screenplay import ScreenPlay
"""
        expected_imports = """
from output.screenplay import ScreenPlay
"""
        refactored_imports = generator.refactor_packages(imports, "output")
        self.assertEqual(refactored_imports, expected_imports)

    def test_refactor_packages_action_all_imports(self):
        generator = SkeletonGenerator("../technical domain/output")
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

    def test_get_actor_implementation(self):
        a_scene = Scene("output")
        line_1 = """
            GIVEN <Jack Donald> who can <buy some beers>
            WHEN <Jack Donald> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack Donald> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            """
        a_scene.add_moliere_script("act 1 - scene #1 - line #1", line_1)
        a_scene.generate_screenplay(regenerate_project=True)
        jack_donald = a_scene.generator.get_actor_implementation("Jack Donald")
        expected_result = {
                "package": "output.actors",
                "class_name": "JackDonald",
                "inherits from": ["Actor"],
                "properties": [],
                "methods": [
                    {"name": "__init__", "parameters": [], "return type": "", "code": "pass"},
                    {"name": "buy_some_beers",
                     "parameters": [],
                     "return type": "bool",
                     "code": """        print("some code needs to be added in JackDonald.buy_some_beers to interact with the element is true")
        return False
"""},
                    {"name": "go_to_the_pub",
                     "parameters": [],
                     "return type": "bool",
                     "code": """        print("some code needs to be added in JackDonald.go_to_the_pub to interact with the element is true")
        return False
"""},
                    {"name": "order",
                     "parameters": [],
                     "return type": "bool",
                     "code": """        print("some code needs to be added in JackDonald.order to interact with the element is true")
        return False
"""}
                ]
            }
        diff = DeepDiff(jack_donald, expected_result, ignore_order=True)
        self.assertEqual(diff, {})
