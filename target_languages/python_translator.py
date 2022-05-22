from os import makedirs

import unicodedata

from extract_objects import extract_value_between


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


class ClassContentManager:
    def __init__(self, target_location: str, tab_size: int = 4):
        self.target_location = target_location
        self.tabs = " " * tab_size
        self.the_class = {}

    def generate_constructor(self, properties: [dict]) -> str:
        """
        todo add "super.__init__(self)" for each ancestor
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

    def set_class_from_file(self, class_path: str) -> dict:
        class_content = []
        with open(class_path, "r") as class_file:
            class_content = class_file.read().splitlines()
            class_file.close()
        return self.set_class_from_string(class_path, class_content)

    def write_file_from_class(self, class_path: str):
        """
        write this class at class_path
        :param class_path: output path - folders must already exist
        :return:
        """
        lines = ""
        if len(self.the_class["imports"]) > 0:
            lines = "\n".join(self.the_class["imports"]) + "\n\n\n"
        if len(self.the_class["inherits from"]) > 0:
            lines += f"class {self.the_class['class_name']} ({', '.join(self.the_class['inherits from'])}):"
        else:
            lines += f"class {self.the_class['class_name']}\n"
        lines += self.the_class["lines before fist method"]
        for method in self.the_class["methods"]:
            lines += f"{self.tabs}def {method['name']}({', '.join(method['parameters'])}):\n"
            lines += f"{method['code']}\n"

        with open(class_path, "w") as class_file:
            class_file.write(lines)
            class_file.close()

    def set_class_from_string(self, class_path: str, class_content: [str]) -> dict:
        """
        generates a JSON from a class_content
        :param class_path:
        :param class_content: array that holds every lines of code from a well formed class - must be PEP8 compliant
        :return:
        """
        current_line = 0
        self.the_class = {"package": ".".join(class_path.split("/")[:1])}
        line = class_content[current_line]
        current_line += 1
        # process imports
        imports = []
        while not line.startswith("class"):
            if line.startswith("from") or line.startswith("import"):
                imports.append(line)
            else: # todo handle code before class
                pass
            line = class_content[current_line]
            current_line += 1
        self.the_class["imports"] = imports
        # process class
        class_definition = line
        words = class_definition.split(" ")
        self.the_class["class_name"] = words[1]
        try:
            super_classes = extract_value_between(line, "(", ")")
            self.the_class["inherits from"] = super_classes.split(",")
        except IndexError:  # if there is no inheritance
            self.the_class["inherits from"] = []
        # read lines until the 1st method
        line = class_content[current_line]
        current_line += 1
        lines_before_first_method = ""
        while not line.startswith(f"{self.tabs}def"):
            lines_before_first_method += line + "\n"
            line = class_content[current_line]
            current_line += 1
        self.the_class["lines before fist method"] = lines_before_first_method
        # process methods
        self.the_class["methods"] = []
        while current_line < len(class_content):
            # process method name
            method_name = extract_value_between(line, "def", "(").strip()
            method_returns = line.split("->")
            return_type = ""
            if len(method_returns) > 1:
                return_type = method_returns[1]
            # process params
            method_parameters = extract_value_between(line, "(", ")")
            params = []
            for param in method_parameters.split(","):
                params.append(param.strip())
            # process lines of code
            line = class_content[current_line]
            current_line += 1
            method_code = ""
            while current_line < len(class_content) and not line.startswith(f"{self.tabs}def"):
                method_code += line + "\n"
                line = class_content[current_line]
                current_line += 1
            if current_line == len(class_content):
                method_code += line + "\n"
            method_code = self.remove_empty_lines_at_end_of_code(method_code)
            # handle properties in __init__
            if method_name == "__init__":
                properties = self.extract_properties(method_code)
                self.the_class["properties"] = properties
            # record method
            self.add_method({"name": method_name,
                             "parameters": params,
                             "return type": return_type,
                             "code": method_code})
        return self.the_class

    def add_method(self, method: dict):
        """
        add a method in the class
        :param method: {"name": method_name,
                        "parameters": params,
                        "code": method_code}
        :return:
        """
        self.the_class["methods"].append(method)

    def remove_empty_lines_at_end_of_code(self, method_code: str):
        """
        removes empty lines at the end
        todo extend "\n" to "^ *\n$" in case there would be blank lines
        :param method_code:
        :return:
        """
        lines = method_code.split(("\n"))
        last_line = -1
        while lines[:last_line] == "\n":
            last_line -= 1
        return "\n".join(lines[:last_line])

    def extract_properties(self, method_code: str):
        """
        looking for "self\.(.*)=(.*)$" to extract properties ($1) in the method code
        default value could be ($2) - /!\ not sure about this
        :param method_code:
        :return:
        """
        return []


if __name__ == '__main__':
    test_class = """from output.elements.element import Element
from output.screenplay import ScreenPlay


class Question (ScreenPlay):
    def __init__(self, name: str):
        super.__init__(self, name)
        pass

    def about_the_state_of(self, an_element: Element):
        pass"""
    question_cg = ClassContentManager(".")
    # cg.serialize_class_definition(json_class_example)
    question_cg.set_class_from_string(".", test_class.split("\n"))
    question_cg.write_file_from_class(f"output/test_question.py")
