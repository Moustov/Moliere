from screenplay_specific_domain.extract_objects import extract_screenplay_objects
from screenplay_specific_domain.skeleton_generator import SkeletonGenerator


def generate_screenplay(a_scene: str, regenerate_project: bool = False) -> [str]:
    """

    :param a_scene: Moliere's BDDeg.
            GIVEN <Jack Donald> who can <browse the web> and <call HTTP APIs> and <go to the pub>
            WHEN <Jack Donald> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack Donald> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
    :param regenerate_project: todo propose regenerating/versioning/overlapping
    :return: compatible with ScreenPlay.play_test_script()
    """
    my_screenplay_objects = extract_screenplay_objects(a_scene)
    generator = SkeletonGenerator("output")
    generator.generate_skeleton_parts(my_screenplay_objects, regenerate_project)
    scenarios = generator.generate_questions()


if __name__ == '__main__':
    my_scene = """
            GIVEN <Jack Donald> who can <browse the web> and <call HTTP APIs> and <go to the pub>
            WHEN <Jack Donald> does <go to the pub> at <The Sheep's Head Pub>
                AND <order> with <999 beers>
                THEN <Jack Donald> checks <the total amount> is <999 × 2.59 EUR>
                          THANKS TO <the total amount> FOUND ON <the bill>
            """
    generate_screenplay(my_scene, True)
