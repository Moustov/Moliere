import re

from skeleton_generator import generate_skeleton


def clean_actor_in_given(actor_in_given: str):
    raw_actor = actor_in_given.split("GIVEN")[1]
    left_right = raw_actor.split("<")
    actor = left_right[1].split(">")[0]
    return actor


def clean_ability_in_given(ability_in_given):
    left_right = ability_in_given.split("<")
    ability = left_right[1].split(">")[0]
    return ability


def clean_task_in_when(task_in_when: str):
    return "Task"


def clean_parameter_in_when(param_in_when: str):
    return "Parameters"


def generate_screenplay(a_scene: str):
    my_screenplay_objects = extract_screenplay_objects(a_scene)
    generate_skeleton(my_screenplay_objects)


def extract_screenplay_objects(my_scene: str) -> dict:
    """
    > GIVEN <Actor> who can <Ability…>
    > WHEN <Actor> does <Task(Parameters)>
    > THEN <Actor> checks <Question> is <Assertion… on Answer>
    > THANKS TO <element> FOUND ON <screen>
    :param my_scene:
    :return:
    """
    screen_play_generated_parts = {
        "actors": [],
        "facts": [],
        "tasks": [],
        "questions": [],
        "elements": [],
        "screens": [],
        "abilities": [],
        "actions": []
    }
    if my_scene is None or my_scene == "":
        return screen_play_generated_parts

    given_whenthen = my_scene.split("WHEN")
    given_part = given_whenthen[0]
    whenthen_part = given_whenthen[1].split("THEN")
    when_part = whenthen_part[0]
    then_part = whenthen_part[1]

    given_parts = given_part.split("who can")
    screen_play_generated_parts["actors"].append(clean_actor_in_given(given_parts[0]))
    screen_play_generated_parts["abilities"].append(clean_ability_in_given(given_parts[1]))
    does_parts = when_part.split("does")
    task = does_parts[1].split("<")
    screen_play_generated_parts["actions"].append(
        {"do": clean_task_in_when(task[1]), "direct object": clean_parameter_in_when(task[2])}
    )
    screen_play_generated_parts["tasks"].append(clean_task_in_when(task[1]))
    return screen_play_generated_parts


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
    extract_screenplay_objects(my_scene)
