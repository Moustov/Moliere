def extract_value_between(raw_string, left_delimiter, right_delimiter) -> str:
    left_right = raw_string.split(left_delimiter)
    value = left_right[1].split(right_delimiter)
    return value[0]


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

    screen_play_generated_parts["actors"].append(extract_value_between(a_scene, "GIVEN <", "> who"))
    screen_play_generated_parts["abilities"].append(extract_value_between(a_scene, "who can <", ">"))
    an_action = {"do": extract_value_between(a_scene, "does <", ">"),
                 "direct object": extract_value_between(a_scene, "with <", ">")
                 }
    screen_play_generated_parts["actions"].append(an_action)
    screen_play_generated_parts["tasks"].append(screen_play_generated_parts["actions"][0]["do"])
    a_question = {"check": extract_value_between(a_scene, "checks <", ">"),
                  "is": extract_value_between(a_scene, "is <", ">")}
    screen_play_generated_parts["questions"].append(a_question)
    screen_play_generated_parts["screens"].append(extract_value_between(a_scene, "FOUND ON <", ">"))
    an_element = {"item": extract_value_between(a_scene, "THANKS TO <", ">"),
                  "screen": screen_play_generated_parts["screens"][0]}
    screen_play_generated_parts["elements"].append(an_element)
    return screen_play_generated_parts


if __name__ == '__main__':
    """
    main to script extract/generate
    => generates a JSON in a file/stdout
    """
    my_scene = """
    GIVEN <Jack> who can <browse the web> and <call HTTP APIs>
    WHEN <Jack> does <walk into> <The Sheep's Head Pub>
        AND does <order> <999 beers>
        THEN <Jack> checks <the bill's total amount> <is 999 × 2.59 EUR>
    """
    screenplay_generated_parts = extract_screenplay_objects(my_scene)
    print(screenplay_generated_parts)
