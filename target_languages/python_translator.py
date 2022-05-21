from os import makedirs

import unicodedata


def translate_to_python_names(a_name) -> str:
    """
    translates a string into something compatible with python
    see https://stackoverflow.com/questions/2365411/convert-unicode-to-ascii-without-errors-in-python
    todo: use phonetic eg. if japanese "あ" could be translated to "a"
    (see eg https://programminghistorian.org/en/lessons/transliterating)
    :param a_name:
    :return:
    """
    return unicodedata.normalize('NFKD', a_name).encode('ascii', 'ignore').decode()


def generate_valid_class_name(class_name: str) -> str:
    """Turns a class name into PEP8 standard (ie. with CamelCase)
    :param class_name: a class name
    """
    class_name = translate_to_python_names(class_name)
    words = class_name.split(" ")
    res = ""
    for word in words:
        word = word.replace("'", "")
        if word[0].isdigit():
            res += "Some" + word
        else:
            res += word[0].upper() + word[1:]
    return res


def generate_valid_method_name(method_name: str) -> str:
    """
    Turns a method_name name into PEP8 standard (ie. with '_')
    :param method_name:
    :return:
    """
    method_name = translate_to_python_names(method_name)
    res = ""
    for c in method_name:
        if ord('0') <= ord(c) <= ord('9') \
                or ord('a') <= ord(c) <= ord('z') \
                or ord('A') <= ord(c) <= ord('Z'):
            res += c
        elif ord(c) == ord("*") or ord(c) == ord("×"):
            res += "x"
        else:
            res += "_"
    return res


class ClassGenerator:
    def __init__(self, target_location: str, tab_size: int = 4):
        self.target_location = target_location
        self.tabs = " " * tab_size

    def generate_constructor(self, properties: [dict]) -> str:
        """
        :param tab_size:
        :param properties:
        :return:
        """
        parameters = ""
        initialize_code = ""
        for a_property in properties:
            if "default value" in a_property.keys() and a_property["default value"] is not None:
                parameters += f", {a_property['name']}=\"{a_property['default value']}\""
            else:
                parameters += ", " + a_property["name"]
            initialize_code += f"\n{self.tabs}{self.tabs}self.{a_property['name']} = {a_property['name']}"
        code = f"{self.tabs}def __init__(self{parameters}):{initialize_code}\n"
        return code

    def generate_method(self, a_method_description: [dict]) -> str:
        """
        :param a_method_description:
        :return:
        """
        comma = ""
        if len(a_method_description['parameters']) > 0:
            comma = ", "
        code = f"{self.tabs}def {a_method_description['name']}(self{comma}{', '.join(a_method_description['parameters'])}):\n" \
               f"{self.tabs}{self.tabs}{a_method_description['code']}\n"
        return code

    def serialize_class_definition(self, json_class: dict):
        """
        writes a file from a json_class
        :param json_class: example = {
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
        :return:
        """
        class_file_path = json_class["package"].split(".")
        path = "/".join(class_file_path)
        makedirs(self.target_location + "/" + path, exist_ok=True)
        with open(self.target_location + "/" + path + "/" + json_class["class_name"] + ".py", "w") as class_file:
            ancestors_string = ""
            if len(json_class["inherits from"]) > 0:
                ancestors_string = "(" + ", ".join(json_class["inherits from"]) + ")"
            class_header = f"class {json_class['class_name']} {ancestors_string}:"
            init_method = "\n" + self.generate_constructor(json_class["properties"])
            methods_code = ""
            for method in json_class["methods"]:
                methods_code += "\n" + self.generate_method(method)
            class_file.write(class_header)
            class_file.write(init_method)
            class_file.write(methods_code)


if __name__ == '__main__':
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
    class_generator = ClassGenerator(".", 4)
    class_generator.serialize_class_definition(json_class_example)
