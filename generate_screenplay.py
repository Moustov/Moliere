from extract_objects import extract_screenplay_objects
from skeleton_generator import generate_skeleton


def generate_screenplay(a_scene: str):
    my_screenplay_objects = extract_screenplay_objects(a_scene)
    generate_skeleton(my_screenplay_objects)


#
# def generate_screenplay2(my_scene: str) -> dict:
#     """
#
# > GIVEN <Actor> who can <Ability…>
# > WHEN <Actor> does <Task(Parameters)>
# > THEN <Actor> checks <Question> is <Assertion… on Answer>
# > THANKS TO <element> FOUND ON <screen>
#     :param my_scene:
#     :return:
#     """
#     screen_play_generated_parts = {}
#     screen_play_parts = my_scene.split("WHEN")
#     given_part = screen_play_parts[0]
#     when_part = screen_play_parts[1]
#     print(given_part)
#     given_parts = given_part.split("who can")
#     actors = given_parts[0]
#     facts = given_parts[1]
#     print(when_part)
#     screen_play_generated_parts[actors]
#     return screen_play_generated_parts


if __name__ == '__main__':
    my_scene = """
GIVEN <Jack> who can <browse the web> and <call HTTP APIs>
WHEN <Jack> does <walk into> <The Sheep's Head Pub>
    AND does <order> <999 beers>
    THEN <Jack> checks <the bill's total amount> <is 999 × 2.59 EUR>
"""
    generate_screenplay(my_scene)
