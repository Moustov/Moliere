from unittest import TestCase

from target_languages.python_translator import ClassGenerator


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
        cg = ClassGenerator(".")
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
        cg = ClassGenerator(".")
        init_code = cg.generate_constructor(json_class_example["properties"])
        expected_value = """    def __init__(self, prop1, prop2):
        self.prop1 = prop1
        self.prop2 = prop2
"""
        self.assertEqual(init_code, expected_value)
