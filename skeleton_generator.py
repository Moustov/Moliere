def generate_actors_skeleton(param, regenerate_project):
    pass


def generate_facts_skeleton(param, regenerate_project):
    pass


def generate_tasks_skeleton(param, regenerate_project):
    pass


def generate_actions_skeleton(param, regenerate_project):
    pass


def generate_abilities_skeleton(param, regenerate_project):
    pass


def generate_screens_skeleton(param, regenerate_project):
    pass


def generate_elements_skeleton(param, regenerate_project):
    pass


def generate_questions_skeleton(param, regenerate_project):
    pass


def generate_skeleton(screenplay_objects: dict, regenerate_project: bool = False):
    """
    generates files that implement the classes from the screenplay Design Pattern (DP)
    - if project is empty => generates root classes from the DP
    - if project is not empty and not regenerate_project => adds objects to the existing project
    :param regenerate_project: forces project generation only from screenplay_objects
    :param screenplay_objects:
    :return:
    """
    generate_actors_skeleton(screenplay_objects["actors"], regenerate_project)
    generate_facts_skeleton(screenplay_objects["facts"], regenerate_project)
    generate_tasks_skeleton(screenplay_objects["tasks"], regenerate_project)
    generate_questions_skeleton(screenplay_objects["questions"], regenerate_project)
    generate_elements_skeleton(screenplay_objects["elements"], regenerate_project)
    generate_screens_skeleton(screenplay_objects["screens"], regenerate_project)
    generate_abilities_skeleton(screenplay_objects["abilities"], regenerate_project)
    generate_actions_skeleton(screenplay_objects["actions"], regenerate_project)


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

    generate_skeleton(screenplay_generated_parts)
