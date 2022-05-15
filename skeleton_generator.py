import os
import shutil


# OS = platform.system()
# if OS == "Windows":
#     PATH_SEPARATOR = "\\"
# elif OS == "Darwin":
#     PATH_SEPARATOR = ":"
# elif OS == "Linux":
#     PATH_SEPARATOR = "/"


def change_to_camel_case(class_name: str):
    words = class_name.split(" ")
    res = ""
    for word in words:
        res += word[0].upper() + word[1:]
    return res


def generate_skeleton_part(part: dict, part_type: str, regenerate_project: bool):
    shutil.copyfile(os.path.normcase(f"canvas/{part_type.lower()}.py"), os.path.normcase(f"output/{part_type.lower()}.py"))
    for class_name in part:
        class_canvas = ""
        class_name = change_to_camel_case(class_name)
        with open(os.path.normcase("canvas/class_canvas.py"), "r") as class_canvas_file:
            class_canvas = class_canvas_file.read()
        class_canvas = class_canvas.replace("TheClassType", part_type)
        class_canvas = class_canvas.replace("TheClass", class_name)
        class_canvas = class_canvas.replace("#YOUR IMPORTS", f"from output.{class_name} import {part_type}")
        with open(os.path.normcase(f"output/{class_name}.py"), "w") as class_file:
            class_file.write(class_canvas)


def generate_skeleton_complex_part(param, param1, regenerate_project):
    pass


def generate_skeleton_parts(screenplay_objects: dict, regenerate_project: bool = False):
    """
    generates files that implement the classes from the output Design Pattern (DP)
    - if project is empty => generates root classes from the DP
    - if project is not empty and not regenerate_project => adds objects to the existing project
    :param regenerate_project: forces project generation only from screenplay_objects
    :param screenplay_objects:
    :return:
    """
    generate_skeleton_part(screenplay_objects["actors"], "Actor", regenerate_project)
    generate_skeleton_part(screenplay_objects["facts"], "Fact", regenerate_project)
    generate_skeleton_part(screenplay_objects["tasks"], "Task", regenerate_project)
    generate_skeleton_complex_part(screenplay_objects["questions"], "Question", regenerate_project)
    generate_skeleton_complex_part(screenplay_objects["elements"], "Element", regenerate_project)
    generate_skeleton_complex_part(screenplay_objects["abilities"], "Ability", regenerate_project)
    generate_skeleton_part(screenplay_objects["screens"], "Screen", regenerate_project)
    generate_skeleton_complex_part(screenplay_objects["actions"], "Action", regenerate_project)


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

    generate_skeleton_parts(screenplay_generated_parts)
