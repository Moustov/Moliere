from extract_objects import extract_screenplay_objects
from skeleton_generator import generate_skeleton


def generate_screenplay(a_scene: str):
    my_screenplay_objects = extract_screenplay_objects(a_scene)
    generate_skeleton(my_screenplay_objects)


if __name__ == '__main__':
    my_scene = """
            GIVEN <Jack> who can <browse the web> and <call HTTP APIs> and <go to the pub>
            WHEN <Jack> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            """
    generate_screenplay(my_scene)
