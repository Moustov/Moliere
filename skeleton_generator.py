import os
import shutil


def change_to_camel_case(class_name: str):
    """Turns a class name into PEP8 standard (ie. with CamelCase)
    :param class_name: a class name
    """
    words = class_name.split(" ")
    res = ""
    for word in words:
        res += word[0].upper() + word[1:]
    return res

class SkeletonGenerator:
    def __init__(self, output_dir: str):
        self.output_directory = output_dir
        self.packages = []

    def generate_skeleton(self):
        """Copy base classes to self.output_directory"""
        self.packages = []
        self.generate_skeleton_with_base_class("actor")
        self.generate_skeleton_with_base_class("ability", "abilities")
        self.generate_skeleton_with_base_class("action")
        self.generate_skeleton_with_base_class("element")
        self.generate_skeleton_with_base_class("fact")
        self.generate_skeleton_with_base_class("question")
        self.generate_skeleton_with_base_class("screen")
        self.generate_skeleton_with_base_class("task")
        shutil.copyfile(os.path.normcase(f"canvas/screenplay.py"),
                        os.path.normcase(f"{self.output_directory}/screenplay.py"))

    def update_imports(self, part_type_folder_name: str, base_class: str):
        with open(os.path.normcase(f"{self.output_directory}/{part_type_folder_name}/{base_class}.py"), "r") as class_file:
            the_class = class_file.read()
            the_class = self.refactor_packages(the_class)
        with open(os.path.normcase(f"{self.output_directory}/{part_type_folder_name}/{base_class}.py"),
                  "w") as class_file:
            class_file.write(the_class)

    def generate_skeleton_with_base_class(self, base_class: str, folder_name: str = None):
        """Copy a base class
        :param base_class: one of the SPDP base class
        :param folder_name: this string is to be used as the destination folder
        """
        self.packages.append({"base_class": base_class, "folder_name": folder_name})
        part_type_folder_name = ""
        if folder_name is not None:
            part_type_folder_name = folder_name
        else:
            part_type_folder_name = f"{base_class}s"
        if not os.path.exists(self.output_directory + f"/{part_type_folder_name}"):
            os.mkdir(self.output_directory + f"/{part_type_folder_name}")
            print("Directory ", self.output_directory + f"/{part_type_folder_name}", " Created ")

        shutil.copyfile(os.path.normcase(f"canvas/__init__.py"),
                        os.path.normcase(f"{self.output_directory}/{part_type_folder_name}/__init__.py"))
        shutil.copyfile(os.path.normcase(f"canvas/{base_class.lower()}.py"),
                        os.path.normcase(f"{self.output_directory}/{part_type_folder_name}/{base_class.lower()}.py"))
        self.update_imports(part_type_folder_name, base_class)

    def generate_skeleton_part(self, the_part: dict, part_type: str, regenerate_project: bool):
        """Generate the classes from the_part
        :param regenerate_project:
        :param part_type:
        :param the_part:
        """
        part_type_folder_name = f"{part_type.lower()}s"
        if not os.path.exists(self.output_directory + f"/{part_type_folder_name}"):
            os.mkdir(self.output_directory + f"/{part_type_folder_name}")
            print("Directory ", self.output_directory + f"/{part_type_folder_name}", " Created ")
        shutil.copyfile(os.path.normcase(f"canvas/{part_type.lower()}.py"),
                        os.path.normcase(f"{self.output_directory}/{part_type_folder_name}/{part_type.lower()}.py"))
        for class_name in the_part:
            class_canvas = ""
            class_name = change_to_camel_case(class_name)
            with open(os.path.normcase("canvas/class_canvas.py"), "r") as class_canvas_file:
                class_canvas = class_canvas_file.read()
            class_canvas = class_canvas.replace("TheClassType", part_type)
            class_canvas = class_canvas.replace("TheClass", class_name)
            class_canvas = class_canvas.replace("#YOUR IMPORTS",
                                                f"from {self.output_directory}.{part_type_folder_name}.{part_type.lower()} import {part_type}")
            with open(os.path.normcase(f"{self.output_directory}/{part_type_folder_name}/{class_name}.py"),
                      "w") as class_file:
                class_file.write(class_canvas)

    def generate_skeleton_complex_part(self, the_part: dict , part_type: str, regenerate_project: bool):
        """
        same as generate_skeleton_part except it handles objects with parameters such as questions, elements, abilities and actoins
        :param the_part:
        :param part_type:
        :param regenerate_project:
        :return:
        """
        pass

    def generate_skeleton_parts(self, screenplay_objects: dict, regenerate_project: bool = False):
        """
        generates files that implement the classes from the output Design Pattern (DP)
        - if project is empty => generates root classes from the DP
        - if project is not empty and not regenerate_project => adds objects to the existing project
        :param output_directory:
        :param regenerate_project: forces project generation only from screenplay_objects
        :param screenplay_objects:
        :return:
        """
        if regenerate_project:
            shutil.rmtree(self.output_directory)
            if not os.path.exists(self.output_directory):
                os.mkdir(self.output_directory)
                print("Directory ", self.output_directory, " Created ")
        self.generate_skeleton()
        self.generate_skeleton_part(screenplay_objects["actors"], "Actor", regenerate_project)
        self.generate_skeleton_part(screenplay_objects["facts"], "Fact", regenerate_project)
        self.generate_skeleton_part(screenplay_objects["tasks"], "Task", regenerate_project)
        self.generate_skeleton_complex_part(screenplay_objects["questions"], "Question", regenerate_project)
        self.generate_skeleton_complex_part(screenplay_objects["elements"], "Element", regenerate_project)
        self.generate_skeleton_complex_part(screenplay_objects["abilities"], "Ability", regenerate_project)
        self.generate_skeleton_part(screenplay_objects["screens"], "Screen", regenerate_project)
        self.generate_skeleton_complex_part(screenplay_objects["actions"], "Action", regenerate_project)

    def refactor_packages(self, the_class: str) -> str:
        return the_class


if __name__ == '__main__':
    """
    main to script extract/generate
    => generates a skeleton from a JSON file/stdin
    """
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
    generator = SkeletonGenerator("output")
    generator.generate_skeleton_parts(screenplay_generated_parts, True)
