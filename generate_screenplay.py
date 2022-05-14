
def generate_screenplay(my_scene: str) -> dict:
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
    return screen_play_generated_parts


def generate_screenplay2(my_scene: str) -> dict:
    """

> GIVEN <Actor> who can <Ability…>
> WHEN <Actor> does <Task(Parameters)>
> THEN <Actor> checks <Question> is <Assertion… on Answer>
> THANKS TO <element> FOUND ON <screen>
    :param my_scene:
    :return:
    """
    screen_play_generated_parts = {}
    screen_play_parts = my_scene.split("WHEN")
    given_part = screen_play_parts[0]
    when_part = screen_play_parts[1]
    print(given_part)
    given_parts = given_part.split("who can")
    actors = given_parts[0]
    facts = given_parts[1]
    print(when_part)
    screen_play_generated_parts[actors]
    return screen_play_generated_parts


if __name__ == '__main__':
    my_scene = """
GIVEN <Jack> who can <browse the web> and <call HTTP APIs>
WHEN <Jack> does <walk into> <The Sheep's Head Pub>
    AND does <order> <999 beers>
    THEN <Jack> checks <the bill's total amount> <is 999 × 2.59 EUR>
"""
    generate_screenplay(my_scene)
