from unittest import TestCase

from deepdiff import DeepDiff

from target_languages.python_translator import ClassContentManager


class Test(TestCase):
    def test_generate_constructor_default_values(self):
        json_class_example = {
            "package": "output.folder_location",
            "class_name": "MyClass",
            "inherits from": ["MyClass1", "MyClass2"],
            "properties": [
                {"name": "prop1", "default value": "v1"},
                {"name": "prop2", "default value": "v2"}
            ],
            "methods": [
                {"name": "m1", "parameters": ["p1", "p2", "p3"], "code": "print('hello world')"},
                {"name": "m2", "parameters": ["p1"], "code": "print(p1)"}
            ]
        }
        cg = ClassContentManager(".")
        init_code = cg.generate_constructor(json_class_example["properties"])
        expected_value = """    def __init__(self, prop1="v1", prop2="v2"):
        self.prop1 = prop1
        self.prop2 = prop2
"""
        self.assertEqual(init_code, expected_value)

    def test_generate_constructor(self):
        json_class_example = {
            "package": "output.folder_location",
            "class_name": "MyClass",
            "inherits from": ["MyClass1", "MyClass2"],
            "properties": [
                {"name": "prop1"},
                {"name": "prop2"}
            ],
            "methods": [
                {"name": "m1", "parameters": ["p1", "p2", "p3"], "code": "print('hello world')"},
                {"name": "m2", "parameters": ["p1"], "code": "print(p1)"}
            ]
        }
        cg = ClassContentManager(".")
        init_code = cg.generate_constructor(json_class_example["properties"])
        expected_value = """    def __init__(self, prop1, prop2):
        self.prop1 = prop1
        self.prop2 = prop2
"""
        self.assertEqual(init_code, expected_value)


class TestClassContentManager(TestCase):
    def test_set_class_from_string(self):
        test_class = """from output.elements.element import Element
from output.screenplay import ScreenPlay


class Question (ScreenPlay):
    def __init__(self, name: str):
        super.__init__(self, name)
        pass

    def about_the_state_of(self, an_element: Element):
        pass"""
        expected_json_class = {
            "package": ".",
            "imports": ['from output.elements.element import Element', 'from output.screenplay import ScreenPlay'],
            "class_name": "Question",
            "inherits from": ["ScreenPlay"],
            "properties": [],
            "lines before fist method": "",
            "methods": [
                {"name": "__init__", "parameters": ["self", "name: str"], "return type": "",
                 "code": """        super.__init__(self, name)
        pass\n"""},
                {"name": "about_the_state_of", "parameters": ["self", "an_element: Element"], "return type": "",
                 "code": "        pass"}
            ]
        }
        cg = ClassContentManager(".")
        json_class = cg.set_class_from_string(".", test_class.split("\n"))
        diff = DeepDiff(expected_json_class, json_class, ignore_order=True)
        self.assertEqual(diff, {})

    def test_read_write_actor_class(self):
        self.read_write_class("canvas/ability.py", "output/test_ability.py")
        self.read_write_class("canvas/action.py", "output/test_action.py")
        self.read_write_class("canvas/actor.py", "output/test_actor.py")
        self.read_write_class("canvas/class_canvas.py", "output/test_class_canvas.py")
        self.read_write_class("canvas/element.py", "output/test_element.py")
        self.read_write_class("canvas/fact.py", "output/test_fact.py")
        self.read_write_class("canvas/question.py", "output/test_question.py")
        self.read_write_class("canvas/screen.py", "output/test_screen.py")
        self.read_write_class("canvas/task.py", "output/test_task.py")

    def read_write_class(self, input_class_path: str, output_class_path: str):
        cg = ClassContentManager(".")
        cg.set_class_from_file(input_class_path)
        expected_json_class = cg.the_class
        cg.write_file_from_class(output_class_path)
        cg.set_class_from_file(output_class_path)
        diff = DeepDiff(expected_json_class, cg.the_class, ignore_order=True)
        # since the class is generated elsewhere, the package should change
        self.assertEqual(diff, {'values_changed':
                                    {"root['package']":
                                                       {'new_value': 'output',
                                                        'old_value': 'canvas'}}})

    def test_docstring_in_class(self):
        self.read_write_class("canvas/screenplay.py", "output/test_screenplay.py")
