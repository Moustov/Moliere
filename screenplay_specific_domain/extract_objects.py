import re


def extract_value_between(raw_string, left_delimiter, right_delimiter) -> str:
    """
    return the string between left_delimiter and right_delimiter
    :param raw_string:
    :param left_delimiter:
    :param right_delimiter:
    :return:
    """
    left_right = raw_string.split(left_delimiter)
    value = left_right[1].split(right_delimiter)
    return value[0]


def extract_actions(a_scene: str) -> [dict]:
    """
    extract Action-like actions from a_scene string
    :param a_scene: a **Molière** string scenario
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
    :param a_scene: a **Molière** string scenario
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

    :param a_scene: a **Molière** string scenario
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


def remove_dupes(an_array: [str]) -> [str]:
    """
    remove dupes in an_array
    :param an_array:
    :return:
    """
    return list(dict.fromkeys(an_array))


def remove_dupes_in_elements(list_elements: [dict]) -> [dict]:
    """
    remove dupes in a list_elements [{"item": an item, "screen": the Screen-like name onto which an item can be found}*]
    :param list_elements:
    :return:
    """
    elements = []
    res = []
    for element in list_elements:
        if element["item"] not in elements:
            elements.append(element["item"])
            res.append(element)
    return res


def extract_questions(a_scene: str) -> [dict]:
    """

    :param a_scene: a **Molière** string scenario
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
    :param a_scene: a **Molière** string scenario
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
    screen_play_generated_parts["abilities"] = remove_dupes(screen_play_generated_parts["abilities"])
    screen_play_generated_parts["questions"] = extract_questions(a_scene)
    screen_play_generated_parts["screens"].append(extract_value_between(a_scene, "FOUND ON <", ">"))
    screen_play_generated_parts["elements"] += extract_elements(a_scene, screen_play_generated_parts["abilities"],
                                                                screen_play_generated_parts["screens"],
                                                                screen_play_generated_parts["actions"])
    screen_play_generated_parts["elements"] = remove_dupes_in_elements(screen_play_generated_parts["elements"])
    return screen_play_generated_parts


if __name__ == '__main__':
    """
    main to script extract/generate
    => generates a JSON in a file/stdout
    """
    my_scene = """
            GIVEN <Jack> who can <browse the web> and <call HTTP APIs> and <go to the pub>
            WHEN <Jack> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            """
    screenplay_generated_parts = extract_screenplay_objects(my_scene)
    print(screenplay_generated_parts)
