import os
import shutil

from extract_objects import extract_value_between


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
    def __init__(self, output_dir: str, regenerate_project: bool=False):
        self.output_directory = output_dir
        self.packages = []
        self.initiate_skeleton(regenerate_project)

    def initiate_skeleton(self, regenerate_project: bool=False):
        """Copy base classes to self.output_directory"""
        self.packages = []
        if regenerate_project:
            shutil.rmtree(self.output_directory)
            if not os.path.exists(self.output_directory):
                os.mkdir(self.output_directory)
                print("Directory ", self.output_directory, " Created ")

        self.packages.append({"base_class": "Actor", "folder_name": "actors", "file_name": "actor.py"})
        self.packages.append({"base_class": "Fact", "folder_name": "facts", "file_name": "fact.py"})
        self.packages.append({"base_class": "Task", "folder_name": "tasks", "file_name": "task.py"})
        self.packages.append({"base_class": "Question", "folder_name": "questions", "file_name": "question.py"})
        self.packages.append({"base_class": "Element", "folder_name": "elements", "file_name": "element.py"})
        self.packages.append({"base_class": "Ability", "folder_name": "abilities", "file_name": "ability.py"})
        self.packages.append({"base_class": "Screen", "folder_name": "screens", "file_name": "screen.py"})
        self.packages.append({"base_class": "Action", "folder_name": "actions", "file_name": "action.py"})
        self.packages.append({"base_class": "ScreenPlay", "folder_name": "", "file_name": "screenplay.py"})

        self.generate_skeleton_with_base_class("actor", "actors")
        self.generate_skeleton_with_base_class("ability", "abilities")
        self.generate_skeleton_with_base_class("action", "actions")
        self.generate_skeleton_with_base_class("element", "elements")
        self.generate_skeleton_with_base_class("fact", "facts")
        self.generate_skeleton_with_base_class("question", "questions")
        self.generate_skeleton_with_base_class("screen", "screens")
        self.generate_skeleton_with_base_class("task", "tasks")
        shutil.copyfile(os.path.normcase(f"canvas/screenplay.py"),
                        os.path.normcase(f"{self.output_directory}/screenplay.py"))

    def update_imports(self, part_type_folder_name: str, base_class: str):
        the_class = ""
        with open(os.path.normcase(f"{self.output_directory}/{part_type_folder_name}/{base_class}.py"), "r") as class_file:
            the_class = class_file.read()
            the_class = self.refactor_packages(the_class, self.output_directory)
            class_file.close()
        with open(os.path.normcase(f"{self.output_directory}/{part_type_folder_name}/{base_class}.py"),
                  "w") as class_file:
            class_file.write(the_class)
            class_file.close()

    def generate_skeleton_with_base_class(self, base_class: str, folder_name: str = None):
        """Copy a base class
        :param base_class: one of the SPDP base class
        :param folder_name: this string is to be used as the destination folder
        """
        os.makedirs(self.output_directory + f"/{folder_name}", exist_ok=True)

        shutil.copyfile(os.path.normcase(f"canvas/__init__.py"),
                        os.path.normcase(f"{self.output_directory}/{folder_name}/__init__.py"))
        shutil.copyfile(os.path.normcase(f"canvas/{base_class.lower()}.py"),
                        os.path.normcase(f"{self.output_directory}/{folder_name}/{base_class.lower()}.py"))
        self.update_imports(folder_name, base_class)

    def generate_skeleton_part(self, the_part: dict, part_type: str, regenerate_project: bool):
        """Generate the classes from the_part
        :param regenerate_project:
        :param part_type:
        :param the_part:
        """
        part_type_folder_name = self.get_folder_name_from_file_name(the_part)
        os.makedirs(self.output_directory + f"/{part_type_folder_name}", exist_ok=True)
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
        self.generate_skeleton_part(screenplay_objects["actors"], "Actor", regenerate_project)
        self.generate_skeleton_part(screenplay_objects["facts"], "Fact", regenerate_project)
        self.generate_skeleton_part(screenplay_objects["tasks"], "Task", regenerate_project)
        self.generate_skeleton_complex_part(screenplay_objects["questions"], "Question", regenerate_project)
        self.generate_skeleton_complex_part(screenplay_objects["elements"], "Element", regenerate_project)
        self.generate_skeleton_complex_part(screenplay_objects["abilities"], "Ability", regenerate_project)
        self.generate_skeleton_part(screenplay_objects["screens"], "Screen", regenerate_project)
        self.generate_skeleton_complex_part(screenplay_objects["actions"], "Action", regenerate_project)

    def refactor_packages(self, the_class: str, dest_folder: str) -> str:
        """
        turns "from canvas.action import Action" into "from output.actions.action import Action"
        :param the_class:
        :param dest_folder:
        :return:
        """
        final_code = ""
        code_lines = the_class.split("\n")
        for line in code_lines:
            import_clauses = line.split("from")
            the_line = ""
            is_processed = False
            for import_clause in import_clauses:
                if import_clause.find("canvas.") > -1 and import_clause.find("import") > -1:
                    is_processed = True
                    class_name = extract_value_between(import_clause, "canvas.", " import")
                    package_folder = self.get_folder_name_from_file_name(class_name)
                    if package_folder is not None:
                        if package_folder == "":
                            the_line = line.replace("canvas.", f"canvas.{package_folder}")
                        else:
                            the_line = line.replace("canvas.", f"canvas.{package_folder}.")
                    else:
                        raise Exception(f"Package for {class_name} not found")
                if not is_processed:
                    the_line = line
            final_code += the_line.replace("canvas", dest_folder) + "\n"
        final_code = final_code[:-1]
        return final_code

    def get_folder_name_from_file_name(self, file_name_extensionless: str) -> str:
        """
        return the folder name associated with the class
        :param file_name_extensionless:
        :return: None if not found
        """
        for package in self.packages:
            try:
                if package["base_class"].lower() == file_name_extensionless.lower():
                    return package["folder_name"]
            except:
                    print(file_name_extensionless)
        return None


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
