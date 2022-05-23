import os
import shutil
from os import makedirs

from extract_objects import extract_value_between
from target_languages.python_translator import generate_valid_class_name, generate_valid_method_name, \
    ClassContentManager


class SkeletonGenerator:
    """
    generates classes stubs in a target directory from screenplay_generated_parts
    screenplay_generated_parts can be generated with module extract_objects.py

    **code sample** (remove backslashes in myscene):

    ```{code-block} python

    my_scene = \"""
            GIVEN <Jack> who can <browse the web> and <call HTTP APIs> and <go to the pub>
            WHEN <Jack> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            \"""
    screenplay_generated_parts = extract_screenplay_objects(my_scene)

    ```

    screenplay_generated_parts should contain

    ```{code-block} python

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

    ```

    then you may call

    ```{code-block} python

    generator = SkeletonGenerator("output")
    generator.generate_skeleton_parts(screenplay_generated_parts, True)

    ```
    """
    def __init__(self, output_dir: str, regenerate_project: bool = False):
        self.output_directory = output_dir
        self.__packages = []
        self.screenplay_classes = {}
        self.initiate_skeleton(regenerate_project)

    def initiate_skeleton(self, regenerate_project: bool = False):
        """Copy base classes to self.output_directory"""
        print("Initiating skeleton...")
        self.__packages = []
        if regenerate_project:
            shutil.rmtree(self.output_directory)
            if not os.path.exists(self.output_directory):
                os.mkdir(self.output_directory)
                print("Directory ", self.output_directory, " Created ")

        self.__packages.append({"base_class": "Actor", "folder_name": "actors", "file_name": "actor.py"})
        self.__packages.append({"base_class": "Fact", "folder_name": "facts", "file_name": "fact.py"})
        self.__packages.append({"base_class": "Task", "folder_name": "tasks", "file_name": "task.py"})
        self.__packages.append({"base_class": "Question", "folder_name": "questions", "file_name": "question.py"})
        self.__packages.append({"base_class": "Element", "folder_name": "elements", "file_name": "element.py"})
        self.__packages.append({"base_class": "Ability", "folder_name": "abilities", "file_name": "ability.py"})
        self.__packages.append({"base_class": "Screen", "folder_name": "screens", "file_name": "screen.py"})
        self.__packages.append({"base_class": "Action", "folder_name": "actions", "file_name": "action.py"})
        self.__packages.append({"base_class": "ScreenPlay", "folder_name": "", "file_name": "screenplay.py"})
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
        with open(os.path.normcase(f"{self.output_directory}/{part_type_folder_name}"
                                   f"/{base_class}.py"), "r") as class_file:
            the_class = class_file.read()
            the_class = self.refactor_packages(the_class, self.output_directory)
            class_file.close()
        with open(os.path.normcase(f"{self.output_directory}/{part_type_folder_name}/{base_class}.py"),
                  "w") as class_file:
            class_file.write(the_class)
            class_file.close()

    def generate_skeleton_with_base_class(self, base_class: str, folder_name: str = None,
                                          regenerate_project: bool = False):
        """Copy a base class
        :param regenerate_project:
        :param base_class: one of the SPDP base class
        :param folder_name: this string is to be used as the destination folder
        """
        os.makedirs(self.output_directory + f"/{folder_name}", exist_ok=True)
        print("Directory ", self.output_directory + f"/{folder_name}", " Created ")
        shutil.copyfile(os.path.normcase(f"canvas/__init__.py"),
                        os.path.normcase(f"{self.output_directory}/{folder_name}/__init__.py"))
        shutil.copyfile(os.path.normcase(f"canvas/{base_class.lower()}.py"),
                        os.path.normcase(f"{self.output_directory}/{folder_name}/{base_class.lower()}.py"))
        self.update_imports(folder_name, base_class)
        cg = ClassContentManager(f"{self.output_directory}/{folder_name}")
        cg.set_class_from_file(f"{self.output_directory}/{folder_name}/{base_class.lower()}.py")
        self.screenplay_classes[base_class] = cg

    def generate_skeleton_parts_from_items(self, screenplay_package_name: str, screenplay_superclass_name: str,
                                           classes: dict,
                                           regenerate_project: bool):
        """Generate the classes from the_part
        :param classes:
        :param regenerate_project:
        :param screenplay_superclass_name:
        :param screenplay_package_name:
        """
        for class_name in classes:
            self.generate_skeleton_for_an_item(screenplay_package_name, screenplay_superclass_name, class_name)

    def generate_skeleton_questions(self, question_parts: dict, regenerate_project: bool):
        """
        same as generate_skeleton_part except it handles objects with parameters
        such as questions, elements, abilities and actoins
        :param part_type:
        :param regenerate_project:
        :return:
        """
        screenplay_objects = []
        for part in question_parts:
            screenplay_objects.append(part["check"])
        self.generate_skeleton_parts_from_items("elements", "Element", screenplay_objects, regenerate_project)
        # todo generate function from "is"
        for part in question_parts:
            self.add_method_in_class(f"check_{generate_valid_method_name(part['is'])}",
                                     generate_valid_class_name(part['check']), "check")

    def generate_skeleton_parts(self, screenplay_objects: dict, regenerate_project: bool = False):
        """
        generates files that implement the classes from the output Design Pattern (DP)
        - if project is empty => generates root classes from the DP
        - if project is not empty and not regenerate_project => adds objects to the existing project
        :param regenerate_project: forces project generation only from screenplay_objects
        :param screenplay_objects:
        :return:
        """
        self.generate_skeleton_parts_from_items("screens", "Screen", screenplay_objects["screens"], regenerate_project)
        self.generate_skeleton_parts_from_items("abilities", "Ability", screenplay_objects["abilities"], regenerate_project)
        # self.generate_skeleton_parts_from_items("actions", "Action", screenplay_objects["actions"], regenerate_project)
        self.generate_skeleton_parts_from_items("actors", "Actor", screenplay_objects["actors"], regenerate_project)
        # self.generate_skeleton_parts_from_items("elements", "Element", screenplay_objects["elements"], regenerate_project)
        self.generate_skeleton_parts_from_items("facts", "Fact", screenplay_objects["facts"], regenerate_project)
        # self.generate_skeleton_parts_from_items("questions", "Question", screenplay_objects["questions"], regenerate_project)
        # self.generate_skeleton_parts_from_items("screens", "Screen", screenplay_objects["screens"], regenerate_project)
        self.generate_skeleton_parts_from_items("tasks", "Task", screenplay_objects["tasks"], regenerate_project)
        self.generate_skeleton_questions(screenplay_objects["questions"], regenerate_project)
        self.generate_skeleton_elements(screenplay_objects["elements"], regenerate_project)
        # todo handle several actors
        self.generate_skeleton_abilities(screenplay_objects["actors"][0], screenplay_objects["abilities"],
                                         regenerate_project)
        # todo handle several actors
        self.generate_skeleton_actions(screenplay_objects["actors"][0], screenplay_objects["actions"],
                                       regenerate_project)
        self.recording_skeleton()

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
        for package in self.__packages:
            if package["base_class"].lower() == file_name_extensionless.lower():
                return package["folder_name"]
        return None

    def generate_skeleton_elements(self, element_part, regenerate_project):
        screenplay_objects = []
        for part in element_part:
            screenplay_objects.append(part["item"])
            if part["item"] not in self.screenplay_classes.keys():
                self.generate_skeleton_for_an_item("elements", "Element", part["item"])
            if part['screen'] is not None and part["screen"] not in self.screenplay_classes.keys():
                self.generate_skeleton_for_an_item("screens", "Screen", part["screen"])
        self.generate_skeleton_parts_from_items("elements", "Element", screenplay_objects, regenerate_project)
        for part in element_part:
            # todo as per the print hereunder
            if part['screen'] is not None:
                self.register_object_in_a_class(generate_valid_class_name(part['item']),
                                                generate_valid_class_name(part['screen']),
                                                "add_element")
            else:
                print(f"No screen defined for '{generate_valid_class_name(part['item'])}'")

    def generate_skeleton_abilities(self, actor: str, abilities_part, regenerate_project):
        screenplay_objects = []
        for part in abilities_part:
            self.add_method_in_class(generate_valid_method_name(part),
                                     generate_valid_class_name(actor), "interact with")

    def generate_skeleton_actions(self, actor: str, actions_part, regenerate_project):
        screenplay_objects = []
        for part in actions_part:
            screenplay_objects.append(part["direct object"])
        self.generate_skeleton_parts_from_items("actions", "Action", screenplay_objects, regenerate_project)
        for part in actions_part:
            self.add_method_in_class(generate_valid_method_name(part['do']),
                                     generate_valid_class_name(actor), "interact with")

    def register_object_in_a_class(self, an_object: str, a_class: str, method_name: str):
        """
        adds an an_object into a_class(Screen)
        todo decline this method to fit right method according to the item we want to register
           eg: add_element for an element on a Screen / an ability on a Actor...
           notably when an object registers different kinds of items (eg. an Actor)
           we may also try using the super class of an_object to define the right method

        :param method_name: the name of the registering method in an_object
        :param an_object:
        :param a_class:
        :return:
        """
        gcm_a_class = self.screenplay_classes[a_class]
        gcm_an_object = self.screenplay_classes[an_object]
        self.screenplay_classes[a_class] = gcm_a_class.add_registration_in_init(gcm_an_object, method_name)
        print(f">> add object '{an_object}' in the class '{a_class}'")
        self.recording_skeleton()

    def add_method_in_class(self, a_method: str, a_class: str, method_type: str):
        """
        add a_method to a_class
        * if method_type is "check" the new method will return True if the check is OK
        *  if method_type is "interact with" the new method will return True if the the action went fine
        todo add parameters for the new method
        :param method_type: "check" or "interact with"  todo refactor to bool or an enum
        :param a_method:
        :param a_class:
        :return: n/a
        """
        method = {"name": a_method,
                  "parameters": ["self"],
                  "return type": "bool",
                  "code": f"""        print("some code needs to be added in {a_class}.{a_method} to {method_type} the element is true")
        return False\n"""
                  },
        print(f">> Adding method '{a_method}' in the class '{a_class}' that will {method_type} an Element")
        # todo for some reason, method is handled as a tuple - to be solved or leave the added [0]
        self.screenplay_classes[a_class].add_method(method[0])  # [0] added to transform a tuple to a dict
        self.recording_skeleton()

    def generate_skeleton_for_an_item(self, screenplay_package_name: str,
                                      screenplay_superclass_name: str, class_name: str):
        """
        generates a class "class_name" which inherits from screenplay_superclass_name
        under the package screenplay_package_name
        :param screenplay_package_name:
        :param screenplay_superclass_name:
        :param class_name:
        :return:
        """
        print(f"Generating '{class_name}' in {screenplay_package_name}")
        class_canvas = ""
        class_name = generate_valid_class_name(class_name)
        with open(os.path.normcase("canvas/class_canvas.py"), "r") as class_canvas_file:
            class_canvas = class_canvas_file.read()
        class_canvas = class_canvas.replace("TheClassType", screenplay_superclass_name)
        class_canvas = class_canvas.replace("TheClass", class_name)
        class_canvas = class_canvas.replace("#YOUR IMPORTS",
                                            f"from {self.output_directory}.{screenplay_package_name}"
                                            f".{screenplay_superclass_name.lower()} "
                                            f"import {screenplay_superclass_name}")
        with open(os.path.normcase(f"{self.output_directory}/{screenplay_package_name}/{class_name}.py"),
                  "w") as class_file:
            class_file.write(class_canvas)
        cg = ClassContentManager(f"{self.output_directory}/{screenplay_package_name}")
        cg.set_class_from_file(f"{self.output_directory}/{screenplay_package_name}/{class_name}.py")
        self.screenplay_classes[class_name] = cg

    def recording_skeleton(self):
        # print("Recording SPDP generated classes...")
        for a_class_name in self.screenplay_classes:
            a_class = self.screenplay_classes[a_class_name]
            # print("     Writing class", f"{a_class.target_location}/{a_class.the_class['class_name']}.py")
            makedirs(a_class.target_location, exist_ok=True)
            a_class.write_file_from_class(f"{a_class.target_location}/{a_class.the_class['class_name']}.py")
        print("SPDP classes recorded")


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
