import re

from screenplay_specific_domain.extract_objects import extract_value_between, remove_string_dupes_in_array, \
    remove_dupes_in_elements, merge_simple_object, merge_parametrized_object
from screenplay_specific_domain.target_languages.python_translator import generate_valid_class_name


class MoliereParser:
    def __init__(self):
        pass


def extract_actions(a_scene: str) -> [dict]:
    """
    extract Action-like actions from a_scene string
    test coverage: see test_extract_objects_screenplay_with_jack_and_multiple_checks()
    :param a_scene: a **Molière** string scenario (the extended GIVEN/WHEN/THEN )
    :return: a list of actions {"do": something, "direct object": the item onto which something is done}
    """
    res = []
    actions_string = extract_value_between(a_scene, "does ", "THEN")
    raw_action_params = actions_string.split("AND")
    for raw_action_param in raw_action_params:
        raw_action_and_param = re.split("at|with|in", raw_action_param)
        an_action = {"do": extract_value_between(raw_action_and_param[0], "<", ">"),
                     "direct object": extract_value_between(raw_action_and_param[1], "<", ">")
                     }
        res.append(an_action)
    return res


def extract_abilities(a_scene: str) -> [str]:
    """
    extract abilities from a_scene
    test coverage: see test_extract_objects_screenplay_with_jack_and_multiple_checks()
    :param a_scene: a **Molière** string scenario (the extended GIVEN/WHEN/THEN )
    :return: a list of things some Actor-like object is able to do
    """
    res = []
    abilities_string = extract_value_between(a_scene, "who can ", "WHEN")
    raw_abilities = abilities_string.split("and")
    for raw_ability in raw_abilities:
        res.append(extract_value_between(raw_ability, "<", ">"))
    return res


def extract_elements(a_scene, abilities: [], screens: [], actions: [dict]) -> [dict]:
    """
    test coverage: see test_extract_objects_screenplay_with_jack_and_multiple_checks()
    :param a_scene: a **Molière** string scenario (the extended GIVEN/WHEN/THEN )
    :param abilities: known abilities
    :param screens: known screens
    :param actions: known actions {"do": something, "direct object": the item onto which something is done}
    :return: {"item": some element, "screen": the item onto which the item can be found}
    """
    res = []
    for an_ability in abilities:
        an_element = {"item": "element_to_enable_" + an_ability, "screen": None}
        res.append(an_element)
    for an_action in actions:
        an_element = {"item": "element_to_enable_" + an_action["do"], "screen": None}
        res.append(an_element)
        an_element = {"item": "element_to_reach_" + an_action["direct object"], "screen": None}
        res.append(an_element)
    questions_part = a_scene.split("checks")
    questions = questions_part[1].split("AND")
    for question in questions:
        element_on_screen = extract_value_between(question, "THANKS TO", "FOUND ON")
        screen = question.split("FOUND ON")
        an_element = {"item": extract_value_between(element_on_screen, "<", ">"),
                      "screen": extract_value_between(screen[1], "<", ">")}
        res.append(an_element)
    return res


def extract_questions(a_scene: str) -> [dict]:
    """

    test coverage: see test_extract_objects_screenplay_with_jack_and_multiple_checks()
    :param a_scene: a **Molière** string scenario (the extended GIVEN/WHEN/THEN )
    :return: a list of {"check": something, "is": what is to be checked}
    """
    res = []
    questions_string = a_scene.split("checks")
    raw_questions = questions_string[1].split("AND")
    for raw_question in raw_questions:
        # res.append(extract_value_between(raw_question, "<", ">"))
        a_question = {"check": extract_value_between(raw_question, "<", ">"),
                      "is": extract_value_between(raw_question, "is <", ">")}
        res.append(a_question)
    return res


def extract_screenplay_objects(a_scene: str) -> dict:
    """
    > GIVEN <Actor> who can <Ability…>
    > WHEN <Actor> does <Task(Parameters)>
    > THEN <Actor> checks <Question> is <Assertion… on Answer>
    > THANKS TO <element> FOUND ON <screen>
    test coverage: see test_extract_objects_screenplay_with_jack_and_multiple_checks()
    :param a_scene: a **Molière** string scenario (the extended GIVEN/WHEN/THEN )
    :return: a dict with {
        "actors": [],
        "facts": [],
        "tasks": [],
        "questions": [],
        "elements": [],
        "screens": [],
        "abilities": [],
        "actions": []
    }
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
    if a_scene is None or a_scene == "":
        return screen_play_generated_parts
    a_scene = a_scene.replace("\n", " ")
    screen_play_generated_parts["actors"].append(extract_value_between(a_scene, "GIVEN <", "> who"))
    actions = extract_actions(a_scene)
    screen_play_generated_parts["actions"] += actions
    abilities = extract_abilities(a_scene)
    screen_play_generated_parts["abilities"] += abilities
    for action in actions:
        screen_play_generated_parts["abilities"] += [action["do"]]
        screen_play_generated_parts["tasks"].append(action["do"])
    screen_play_generated_parts["abilities"] = remove_string_dupes_in_array(screen_play_generated_parts["abilities"])
    screen_play_generated_parts["questions"] = extract_questions(a_scene)
    screen_play_generated_parts["screens"].append(extract_value_between(a_scene, "FOUND ON <", ">"))
    screen_play_generated_parts["elements"] += extract_elements(a_scene, screen_play_generated_parts["abilities"],
                                                                screen_play_generated_parts["screens"],
                                                                screen_play_generated_parts["actions"])
    screen_play_generated_parts["elements"] = remove_dupes_in_elements(screen_play_generated_parts["elements"])
    return screen_play_generated_parts


def merge_screenplay_objects(scene1: dict, scene2: dict) -> dict:
    """
    merge 2 sets of screenplay objects
    todo see if this function should not be moved in skeleton_generator.py as a method
    :param scene1:
    :param scene2:
    :return: the merged screenplay objects
    """
    res_scene = merge_simple_object("actors", scene1, scene2)
    res_scene = merge_simple_object("facts", res_scene, scene2)
    res_scene = merge_simple_object("tasks", res_scene, scene2)
    res_scene = merge_parametrized_object("questions", res_scene, scene2)
    res_scene = merge_parametrized_object("elements", res_scene, scene2)
    res_scene = merge_simple_object("screens", res_scene, scene2)
    res_scene = merge_simple_object("abilities", res_scene, scene2)
    res_scene = merge_parametrized_object("actions", res_scene, scene2)
    return res_scene


def extract_question_name(a_scene: str) -> str:
    """
    > GIVEN <Actor> who can <Ability…>
    > WHEN <Actor> does <Task(Parameters)>
    > THEN <Actor> checks <Question> is <Assertion… on Answer>
    > THANKS TO <element> FOUND ON <screen>
    test coverage: see test_extract_objects_screenplay_with_jack_and_multiple_checks()
    :param a_scene: a **Molière** string scenario (the extended GIVEN/WHEN/THEN )
    :return:
    """
    # actor_who_checks = extract_value_between(a_scene, "THEN <", "> checks")
    # question = extract_value_between(a_scene, "checks <", "> is")
    # value = extract_value_between(a_scene, "is <", "> THANKS")
    # element = extract_value_between(a_scene, "THANKS TO <", "> FOUND")
    the_question = a_scene.split("THEN")[1]
    question_class_name = generate_valid_class_name(the_question)
    return question_class_name


def extract_task_name(a_scene: str) -> str:
    """
    > GIVEN <Actor> who can <Ability…>
    > WHEN <Actor> does <Task(Parameters)>
    > THEN <Actor> checks <Question> is <Assertion… on Answer>
    > THANKS TO <element> FOUND ON <screen>
    test coverage: see test_extract_objects_screenplay_with_jack_and_multiple_checks()
    :param a_scene: a **Molière** string scenario (the extended GIVEN/WHEN/THEN )
    :return:
    """
    the_task = extract_value_between(a_scene, "WHEN <", "THEN")
    task_class_name = generate_valid_class_name(the_task)
    return task_class_name
