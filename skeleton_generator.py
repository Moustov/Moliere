

def generate_skeleton(screenplay_objects: dict, regenerate_project: bool = False):
    """
    generates files that implement the classes from the screenplay Design Pattern (DP)
    - if project is empty => generates root classes from the DP
    - if project is not empty and not regenerate_project => adds objects to the existing project
    :param regenerate_project: forces project generation only from screenplay_objects
    :param screenplay_objects:
    :return:
    """
    pass


if __name__ == '__main__':
    """
    main to script extract/generate
    => generates a skeleton from a JSON file/stdin
    """
    screenplay_generated_parts = {
        "actors": ["Jack"],
        "facts": [],
        "tasks": ["go to the pub", "order"],
        "questions": [{"check": "the bill's total amount", "is": "is 999 × 2.59 EUR"}],
        "elements": ["The Sheep's Head Pub", "999 beers", "the bill's total amount"],
        "screens": ["receipt"],
        "abilities": ["browse the web", "call HTTP APIs", "go to the pub"],
        "actions": [
            {"do": "go to the pub", "direct object": "The Sheep's Head Pub"},
            {"do": "order", "direct object": "999 beers"}
        ]
    }

    generate_skeleton(screenplay_generated_parts)
