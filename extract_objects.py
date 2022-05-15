import re


def extract_value_between(raw_string, left_delimiter, right_delimiter) -> str:
    left_right = raw_string.split(left_delimiter)
    value = left_right[1].split(right_delimiter)
    return value[0]


def extract_actions(a_scene):
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


def extract_abilities(a_scene: str):
    res = []
    abilities_string = extract_value_between(a_scene, "who can ", "WHEN")
    raw_abilities = abilities_string.split("and")
    for raw_ability in raw_abilities:
        res.append(extract_value_between(raw_ability, "<", ">"))
    return res


def extract_elements(a_scene, abilities: [], screens: [], actions: [], questions: []):
    res = []
    for an_ability in abilities:
        an_element = {"item": an_ability, "screen": None}
        res.append(an_element)
    for an_action in actions:
        an_element = {"item": an_action["do"], "screen": None}
        res.append(an_element)
        an_element = {"item": an_action["direct object"], "screen": None}
        res.append(an_element)
    elements_on_screen = a_scene.split("THANKS TO")[1].split("FOUND ON")
    an_element = {"item": extract_value_between(elements_on_screen[0], "<", ">"),
                  "screen": extract_value_between(elements_on_screen[1], "<", ">")}
    res.append(an_element)
    return res


def remove_dupes(an_array: []):
    return list(dict.fromkeys(an_array))


def remove_dupes_in_elements(list_elements: [dict]):
    elements = []
    res = []
    for element in list_elements:
        if element["item"] not in elements:
            elements.append(element["item"])
            res.append(element)
    return res


def extract_screenplay_objects(a_scene: str) -> dict:
    """
    > GIVEN <Actor> who can <Ability…>
    > WHEN <Actor> does <Task(Parameters)>
    > THEN <Actor> checks <Question> is <Assertion… on Answer>
    > THANKS TO <element> FOUND ON <screen>
    :param a_scene:
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
    a_question = {"check": extract_value_between(a_scene, "checks <", ">"),
                  "is": extract_value_between(a_scene, "is <", ">")}
    screen_play_generated_parts["questions"].append(a_question)
    screen_play_generated_parts["screens"].append(extract_value_between(a_scene, "FOUND ON <", ">"))
    screen_play_generated_parts["elements"] += extract_elements(a_scene, screen_play_generated_parts["abilities"],
                                                                screen_play_generated_parts["screens"],
                                                                screen_play_generated_parts["actions"],
                                                                screen_play_generated_parts["questions"])
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
