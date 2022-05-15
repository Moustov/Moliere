def extract_actor_in_given(actor_in_given: str):
    raw_actor = actor_in_given.split("GIVEN")[1]
    left_right = raw_actor.split("<")
    actor = left_right[1].split(">")[0]
    return actor


def extract_ability_in_given(ability_in_given):
    left_right = ability_in_given.split("<")
    ability = left_right[1].split(">")[0]
    return ability


def extract_task_in_when(raw_task_in_when: str):
    left_right = raw_task_in_when.split(">")
    task = left_right[0]
    return task


def extract_parameter_in_when(raw_param_in_when: str):
    left_right = raw_param_in_when.split(">")
    param = left_right[0]
    return param


def extract_question_in_then(raw_question: str):
    left_right = raw_question.split(">")
    question = left_right[0]
    return question


def extract_assertion_in_then(raw_assertion):
    left_right = raw_assertion.split(">")
    assertion = left_right[0]
    return assertion


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

    given_whenthen = a_scene.split("WHEN")
    given_part = given_whenthen[0]
    whenthen_part = given_whenthen[1].split("THEN")
    when_part = whenthen_part[0]
    then_part = whenthen_part[1]

    given_parts = given_part.split("who can")
    screen_play_generated_parts["actors"].append(extract_actor_in_given(given_parts[0]))
    screen_play_generated_parts["abilities"].append(extract_ability_in_given(given_parts[1]))
    does_parts = when_part.split("does")
    task = does_parts[1].split("<")
    screen_play_generated_parts["actions"].append(
        {"do": extract_task_in_when(task[1]), "direct object": extract_parameter_in_when(task[2])}
    )
    screen_play_generated_parts["tasks"].append(extract_task_in_when(task[1]))

    question_part = then_part.split("<")
    a_question = {"check": extract_question_in_then(question_part[2]), "is": extract_assertion_in_then(question_part[3])}
    screen_play_generated_parts["questions"].append(a_question)
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
